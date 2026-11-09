from flask import Flask, render_template, request, redirect, url_for, flash, Response
import sqlite3
from pathlib import Path
from datetime import datetime, date, timedelta
import csv
import io

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "jeevan_kavach.db"

def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

def init_db():
    with get_db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dose TEXT NOT NULL DEFAULT '',
            schedule TEXT NOT NULL,
            frequency TEXT NOT NULL DEFAULT 'Daily',
            stock INTEGER NOT NULL DEFAULT 0,
            notes TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS dose_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER,
            medicine_name TEXT NOT NULL,
            scheduled_date TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Taken','Missed')),
            logged_at TEXT NOT NULL,
            FOREIGN KEY(medicine_id) REFERENCES medicines(id) ON DELETE SET NULL
        );
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            acknowledged INTEGER NOT NULL DEFAULT 0
        );
        """)

def log_dose(medicine, status):
    now = datetime.now()
    with get_db() as con:
        # Prevent accidental duplicate status entries for the same medicine on the same day/time.
        existing = con.execute("""
            SELECT id FROM dose_logs
            WHERE medicine_id=? AND scheduled_date=? AND scheduled_time=?
            ORDER BY id DESC LIMIT 1
        """, (medicine["id"], date.today().isoformat(), medicine["schedule"])).fetchone()
        if existing:
            con.execute("""
                UPDATE dose_logs SET status=?, logged_at=?
                WHERE id=?
            """, (status, now.isoformat(timespec="seconds"), existing["id"]))
        else:
            con.execute("""
                INSERT INTO dose_logs
                (medicine_id, medicine_name, scheduled_date, scheduled_time, status, logged_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (medicine["id"], medicine["name"], date.today().isoformat(),
                  medicine["schedule"], status, now.isoformat(timespec="seconds")))
        if status == "Missed":
            con.execute("INSERT INTO alerts(message, created_at) VALUES (?, ?)",
                        (f"Missed dose recorded for {medicine['name']}. Review the routine.", now.isoformat(timespec="seconds")))
        elif status == "Taken":
            con.execute("UPDATE medicines SET stock=MAX(stock-1, 0) WHERE id=?", (medicine["id"],))

@app.route("/")
def dashboard():
    today = date.today().isoformat()
    with get_db() as con:
        medicines = con.execute("SELECT * FROM medicines ORDER BY schedule, name").fetchall()
        today_logs = con.execute("SELECT * FROM dose_logs WHERE scheduled_date=? ORDER BY logged_at DESC", (today,)).fetchall()
        recent_logs = con.execute("SELECT * FROM dose_logs ORDER BY logged_at DESC LIMIT 10").fetchall()
        missed_count = con.execute("SELECT COUNT(*) n FROM dose_logs WHERE status='Missed'").fetchone()["n"]
        total_logs = con.execute("SELECT COUNT(*) n FROM dose_logs").fetchone()["n"]
        taken_logs = con.execute("SELECT COUNT(*) n FROM dose_logs WHERE status='Taken'").fetchone()["n"]
        alerts = con.execute("SELECT * FROM alerts WHERE acknowledged=0 ORDER BY created_at DESC LIMIT 5").fetchall()
    today_taken = sum(1 for x in today_logs if x["status"] == "Taken")
    today_missed = sum(1 for x in today_logs if x["status"] == "Missed")
    adherence = round((taken_logs / total_logs) * 100, 1) if total_logs else 0
    low_stock = [m for m in medicines if m["stock"] <= 3]
    now_hm = datetime.now().strftime("%H:%M")
    due = [m for m in medicines if m["schedule"] <= now_hm]
    return render_template("index.html", page="dashboard", medicines=medicines,
        today_logs=today_logs, recent_logs=recent_logs, alerts=alerts,
        today_taken=today_taken, today_missed=today_missed,
        missed_count=missed_count, adherence=adherence, low_stock=low_stock,
        due=due, today=date.today().strftime("%A, %d %B %Y"))

@app.route("/medicines", methods=["GET", "POST"])
def medicines_page():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        dose = request.form.get("dose", "").strip()
        schedule = request.form.get("schedule", "").strip()
        frequency = request.form.get("frequency", "Daily")
        try:
            stock = max(0, int(request.form.get("stock", "0")))
        except ValueError:
            stock = 0
        notes = request.form.get("notes", "").strip()
        if not name or not schedule:
            flash("Medicine name and schedule are required.", "error")
        else:
            with get_db() as con:
                con.execute("""INSERT INTO medicines(name,dose,schedule,frequency,stock,notes,created_at)
                    VALUES(?,?,?,?,?,?,?)""",
                    (name, dose, schedule, frequency, stock, notes, datetime.now().isoformat(timespec="seconds")))
            flash("Medicine saved successfully.", "success")
        return redirect(url_for("medicines_page"))
    with get_db() as con:
        medicines = con.execute("SELECT * FROM medicines ORDER BY schedule, name").fetchall()
    return render_template("index.html", page="medicines", medicines=medicines)

@app.route("/medicines/<int:medicine_id>/edit", methods=["POST"])
def edit_medicine(medicine_id):
    name = request.form.get("name", "").strip()
    dose = request.form.get("dose", "").strip()
    schedule = request.form.get("schedule", "").strip()
    frequency = request.form.get("frequency", "Daily")
    notes = request.form.get("notes", "").strip()
    try:
        stock = max(0, int(request.form.get("stock", "0")))
    except ValueError:
        stock = 0
    if not name or not schedule:
        flash("Name and schedule cannot be empty.", "error")
    else:
        with get_db() as con:
            con.execute("""UPDATE medicines SET name=?,dose=?,schedule=?,frequency=?,stock=?,notes=? WHERE id=?""",
                        (name, dose, schedule, frequency, stock, notes, medicine_id))
        flash("Medicine updated.", "success")
    return redirect(url_for("medicines_page"))

@app.route("/medicines/<int:medicine_id>/delete", methods=["POST"])
def delete_medicine(medicine_id):
    with get_db() as con:
        con.execute("DELETE FROM medicines WHERE id=?", (medicine_id,))
    flash("Medicine deleted.", "success")
    return redirect(url_for("medicines_page"))

@app.route("/dose/<int:medicine_id>/<status>", methods=["POST"])
def mark_dose(medicine_id, status):
    if status not in ("Taken", "Missed"):
        flash("Invalid dose status.", "error")
        return redirect(url_for("dashboard"))
    with get_db() as con:
        medicine = con.execute("SELECT * FROM medicines WHERE id=?", (medicine_id,)).fetchone()
    if not medicine:
        flash("Medicine not found.", "error")
    else:
        log_dose(medicine, status)
        flash(f"{medicine['name']} marked as {status}.", "success" if status == "Taken" else "warning")
    return redirect(request.referrer or url_for("dashboard"))

@app.route("/history")
def history():
    status = request.args.get("status", "All")
    with get_db() as con:
        if status in ("Taken", "Missed"):
            logs = con.execute("SELECT * FROM dose_logs WHERE status=? ORDER BY logged_at DESC", (status,)).fetchall()
        else:
            logs = con.execute("SELECT * FROM dose_logs ORDER BY logged_at DESC").fetchall()
        weekly = con.execute("""
            SELECT substr(scheduled_date,1,7) AS month,
                   COUNT(*) AS total,
                   SUM(CASE WHEN status='Taken' THEN 1 ELSE 0 END) AS taken
            FROM dose_logs GROUP BY substr(scheduled_date,1,7) ORDER BY month DESC LIMIT 6
        """).fetchall()
    return render_template("index.html", page="history", logs=logs, status=status, weekly=weekly)

@app.route("/alerts")
def alerts_page():
    with get_db() as con:
        alerts = con.execute("SELECT * FROM alerts ORDER BY created_at DESC LIMIT 100").fetchall()
    return render_template("index.html", page="alerts", alerts=alerts)

@app.route("/alerts/<int:alert_id>/acknowledge", methods=["POST"])
def acknowledge_alert(alert_id):
    with get_db() as con:
        con.execute("UPDATE alerts SET acknowledged=1 WHERE id=?", (alert_id,))
    flash("Alert acknowledged.", "success")
    return redirect(url_for("alerts_page"))

@app.route("/export.csv")
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Medicine", "Scheduled date", "Scheduled time", "Status", "Logged at"])
    with get_db() as con:
        rows = con.execute("SELECT medicine_name,scheduled_date,scheduled_time,status,logged_at FROM dose_logs ORDER BY logged_at DESC").fetchall()
    for row in rows:
        writer.writerow(list(row))
    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=jeevan_kavach_dose_history.csv"})

@app.route("/health")
def health():
    return {"status": "ok", "app": "Jeevan Kavach"}

init_db()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
