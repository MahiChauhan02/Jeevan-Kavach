# Jeevan Kavach — Full-stack local website

A Flask + SQLite medicine routine tracker with a responsive dashboard.

## Features
- Dashboard cards for medicine count, today's taken/missed entries, and adherence.
- Add, edit, and delete medicines.
- Mark doses as Taken or Missed; entries are saved to SQLite.
- Dose history with Taken/Missed filters and CSV export.
- Low-stock indicators and stored follow-up alerts.
- Responsive layout for desktop and mobile.

## Run on macOS

1. Install Python 3 if needed.
2. Open Terminal in this folder.
3. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

5. Start the website:

   ```bash
   python3 app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.

The SQLite database (`jeevan_kavach.db`) is created automatically beside `app.py`.

## Notes before public deployment
- Change `app.secret_key` to a long random secret and load it from an environment variable.
- Use a production WSGI server instead of Flask's development server.
- Add authentication and per-user authorization before storing real personal/medical data.
- This prototype does not send SMS, WhatsApp, push, or background notifications. It records reminders and dose statuses locally; do not rely on it for medical alerts.
- The AI/medicine-image demonstration from the previous prototype is not included in this starter version. Do not use software outputs to identify pills or make medical decisions.
