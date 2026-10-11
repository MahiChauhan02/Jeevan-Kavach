{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww28600\viewh18000\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import sqlite3\
from pathlib import Path\
from datetime import datetime, date, time\
\
import numpy as np\
import pandas as pd\
import plotly.express as px\
import streamlit as st\
from PIL import Image\
from sklearn.cluster import KMeans\
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor\
from sklearn.preprocessing import StandardScaler\
\
# --------------------------------------------------\
# JEEVAN KAVACH - APP CONFIGURATION\
# --------------------------------------------------\
\
st.set_page_config(\
    page_title="Jeevan Kavach",\
    page_icon="\uc0\u10022 ",\
    layout="wide",\
    initial_sidebar_state="expanded"\
)\
\
BASE = Path(__file__).parent\
DB_PATH = BASE / "jeevan_kavach.db"\
IMAGE_DIR = BASE / "medicine_images"\
IMAGE_DIR.mkdir(exist_ok=True)\
\
# --------------------------------------------------\
# LUXURY EDITORIAL DESIGN\
# --------------------------------------------------\
\
st.markdown("""\
<style>\
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=DM+Sans:wght@400;500;600;700&display=swap');\
\
:root \{\
    --paper: #F7F0E4;\
    --ink: #4B3024;\
    --muted: #806B5C;\
    --gold: #D99032;\
    --line: #DFD1BD;\
\}\
\
html, body, [class*="css"] \{\
    font-family: 'DM Sans', sans-serif;\
\}\
\
.stApp \{\
    background:\
        radial-gradient(ellipse at 20% 0%, #FFFAF0 0%, transparent 48%),\
        var(--paper);\
    color: var(--ink);\
\}\
\
.block-container \{\
    max-width: 1450px;\
    padding-top: 1.4rem;\
\}\
\
h1, h2, h3, .serif \{\
    font-family: 'Bodoni Moda', Georgia, serif !important;\
    color: var(--ink) !important;\
    font-weight: 400 !important;\
\}\
\
.jk-logo \{\
    font-family: 'Bodoni Moda', Georgia, serif;\
    font-size: clamp(25px, 3vw, 43px);\
    font-weight: 400;\
    letter-spacing: -1.5px;\
    color: var(--ink);\
    text-align: center;\
\}\
\
.jk-nav \{\
    display: grid;\
    grid-template-columns: 1fr auto 1fr;\
    align-items: center;\
    gap: 12px;\
    border-bottom: 1px solid var(--line);\
    padding: 8px 0 20px;\
    margin-bottom: 30px;\
\}\
\
.nav-note \{\
    font-size: 11px;\
    color: var(--muted);\
    letter-spacing: 1.5px;\
\}\
\
.kicker \{\
    display: inline-block;\
    border: 1px solid var(--gold);\
    border-radius: 100px;\
    padding: 9px 20px;\
    color: var(--gold);\
    letter-spacing: 2px;\
    font-size: 11px;\
\}\
\
.hero \{\
    padding: clamp(32px, 6vw, 85px) 20px;\
    border: 1px solid var(--line);\
    border-radius: 25px;\
    text-align: center;\
    background: linear-gradient(140deg, #FFFBF3, #F0E5D2);\
    box-shadow: 0 24px 55px rgba(75,48,36,.08);\
    overflow: hidden;\
\}\
\
.hero h1 \{\
    font-size: clamp(42px, 8vw, 100px) !important;\
    line-height: .98 !important;\
    letter-spacing: -3px;\
    margin: 25px auto;\
\}\
\
.hero p \{\
    color: var(--muted);\
    font-family: 'Bodoni Moda', Georgia, serif;\
    font-size: clamp(16px, 2vw, 23px);\
\}\
\
.slide-card \{\
    min-height: 185px;\
    padding: 24px;\
    border: 1px solid var(--line);\
    border-radius: 17px;\
    background: rgba(255,252,245,.72);\
    box-shadow: 0 12px 28px rgba(75,48,36,.05);\
    transition: transform .4s, box-shadow .4s;\
    animation: float-card 6s ease-in-out infinite;\
\}\
\
.slide-card:nth-child(2) \{ animation-delay: .7s; \}\
.slide-card:nth-child(3) \{ animation-delay: 1.4s; \}\
\
.slide-card:hover \{\
    transform: perspective(900px) rotateY(-5deg)\
               rotateX(4deg) translateY(-8px);\
    box-shadow: 0 25px 45px rgba(75,48,36,.14);\
\}\
\
@keyframes float-card \{\
    0%, 100% \{ transform: translateY(0); \}\
    50% \{ transform: translateY(-6px); \}\
\}\
\
.slide-number \{\
    font-size: 11px;\
    letter-spacing: 2px;\
    color: var(--gold);\
\}\
\
.slide-card h3 \{\
    font-size: 25px !important;\
    margin-top: 13px;\
\}\
\
.slide-card p \{\
    color: var(--muted);\
    line-height: 1.7;\
    font-size: 14px;\
\}\
\
.metric-card \{\
    background: rgba(255,252,245,.8);\
    border: 1px solid var(--line);\
    border-radius: 16px;\
    padding: 18px;\
    min-height: 112px;\
\}\
\
.metric-label \{\
    color: var(--muted);\
    font-size: 11px;\
    letter-spacing: 1.5px;\
    text-transform: uppercase;\
\}\
\
.metric-value \{\
    font-family: 'Bodoni Moda', Georgia, serif;\
    font-size: 33px;\
    color: var(--ink);\
    overflow-wrap: anywhere;\
\}\
\
div.stButton > button \{\
    border-radius: 100px;\
    border: 1px solid #CBB79E;\
    background: #FFFAF0;\
    color: var(--ink);\
    transition: all .2s;\
\}\
\
div.stButton > button:hover \{\
    border-color: var(--gold);\
    color: #8A5015;\
    transform: translateY(-1px);\
\}\
\
div.stButton > button[kind="primary"] \{\
    background: var(--ink);\
    color: #FFF8EB;\
    border-color: var(--ink);\
\}\
\
[data-testid="stSidebar"] \{\
    background: #EFE5D5;\
    border-right: 1px solid var(--line);\
\}\
\
hr \{ border-color: var(--line); \}\
\
@media(max-width: 700px) \{\
    .jk-nav \{ grid-template-columns: 1fr; text-align: center; \}\
    .hero h1 \{ letter-spacing: -1px; \}\
    .nav-note \{ text-align: center; \}\
\}\
</style>\
""", unsafe_allow_html=True)\
\
\
# --------------------------------------------------\
# DATABASE\
# --------------------------------------------------\
\
def get_db():\
    con = sqlite3.connect(DB_PATH, timeout=10)\
    con.row_factory = sqlite3.Row\
    return con\
\
\
def initialize_db():\
    with get_db() as con:\
        con.execute("""\
            CREATE TABLE IF NOT EXISTS medicines (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                name TEXT NOT NULL,\
                dose TEXT,\
                schedule TEXT NOT NULL,\
                stock INTEGER DEFAULT 0,\
                contact TEXT DEFAULT '',\
                notes TEXT DEFAULT ''\
            )\
        """)\
\
        con.execute("""\
            CREATE TABLE IF NOT EXISTS logs (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                medicine_id INTEGER,\
                medicine_name TEXT,\
                scheduled_date TEXT,\
                scheduled_time TEXT,\
                status TEXT,\
                logged_at TEXT\
            )\
        """)\
\
        con.execute("""\
            CREATE TABLE IF NOT EXISTS alerts (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                created_at TEXT,\
                message TEXT,\
                acknowledged INTEGER DEFAULT 0\
            )\
        """)\
\
\
initialize_db()\
\
\
def read_table(table):\
    with get_db() as con:\
        return pd.read_sql_query(\
            f"SELECT * FROM \{table\}", con\
        )\
\
\
def record_dose(medicine, status):\
    with get_db() as con:\
        con.execute("""\
            INSERT INTO logs (\
                medicine_id, medicine_name,\
                scheduled_date, scheduled_time,\
                status, logged_at\
            ) VALUES (?, ?, ?, ?, ?, ?)\
        """, (\
            int(medicine["id"]),\
            medicine["name"],\
            date.today().isoformat(),\
            medicine["schedule"],\
            status,\
            datetime.now().isoformat(timespec="seconds")\
        ))\
\
        if status == "Missed":\
            con.execute("""\
                INSERT INTO alerts (created_at, message)\
                VALUES (?, ?)\
            """, (\
                datetime.now().isoformat(timespec="seconds"),\
                f"Review missed-dose entry for \{medicine['name']\}"\
            ))\
\
\
def show_metric(label, value, foot=""):\
    st.markdown(\
        f"""\
        <div class="metric-card">\
            <div class="metric-label">\{label\}</div>\
            <div class="metric-value">\{value\}</div>\
            <div style="font-size:12px;color:#806B5C">\{foot\}</div>\
        </div>\
        """,\
        unsafe_allow_html=True\
    )\
\
\
# --------------------------------------------------\
# DEMO MACHINE-LEARNING MODELS\
# --------------------------------------------------\
\
@st.cache_resource\
def create_models():\
    rng = np.random.default_rng(42)\
    n = 600\
\
    data = pd.DataFrame(\{\
        "hour": rng.integers(5, 24, n),\
        "age": rng.integers(18, 96, n),\
        "missed_history": rng.integers(0, 10, n),\
        "reminder_used": rng.integers(0, 2, n)\
    \})\
\
    score = np.clip(\
        data["missed_history"] * 8\
        + (data["age"] >= 70) * 12\
        + (data["reminder_used"] == 0) * 10\
        + np.abs(data["hour"] - 13) * .6\
        + rng.normal(0, 7, n),\
        0, 100\
    )\
\
    categories = np.where(\
        score >= 65, "High",\
        np.where(score >= 35, "Moderate", "Low")\
    )\
\
    classifier = RandomForestClassifier(\
        n_estimators=100, random_state=42\
    )\
    classifier.fit(data, categories)\
\
    regressor = RandomForestRegressor(\
        n_estimators=100, random_state=42\
    )\
    regressor.fit(data, score)\
\
    cluster_columns = [\
        "hour", "missed_history", "reminder_used"\
    ]\
\
    cluster_scaler = StandardScaler()\
    scaled = cluster_scaler.fit_transform(\
        data[cluster_columns]\
    )\
\
    cluster_model = KMeans(\
        n_clusters=3, random_state=42, n_init=10\
    )\
    cluster_model.fit(scaled)\
\
    return classifier, regressor, cluster_scaler, cluster_model\
\
\
classifier, regressor, cluster_scaler, cluster_model = create_models()\
\
\
# --------------------------------------------------\
# HEADER + NAVIGATION\
# --------------------------------------------------\
\
st.markdown("""\
<div class="jk-nav">\
    <div class="nav-note">THOUGHTFUL DAILY CARE</div>\
    <div class="jk-logo">JEEVAN KAVACH</div>\
    <div class="nav-note" style="text-align:right">HEALTH & SAFETY</div>\
</div>\
""", unsafe_allow_html=True)\
\
with st.sidebar:\
    st.markdown(\
        '<div class="jk-logo" style="font-size:29px;text-align:left">'\
        'Jeevan Kavach</div>',\
        unsafe_allow_html=True\
    )\
    st.caption("Your health. Your routine. Your safety.")\
\
    page = st.radio("EXPLORE", [\
        "Home",\
        "Dashboard",\
        "Medicine Cabinet",\
        "Smart Reminders",\
        "AI Risk & Explanation",\
        "Pattern Clustering",\
        "Missed-dose Escalation",\
        "Voice Reminder",\
        "Medicine Recognition",\
        "Elder-friendly Mode",\
        "Adherence Reports"\
    ])\
\
    st.divider()\
    elder_mode = st.toggle("Elder-friendly mode")\
    if elder_mode:\
        st.markdown("""\
        <style>\
        .stApp, .stApp p, .stApp label \{\
            font-size: 19px !important;\
        \}\
        div.stButton > button \{\
            min-height: 48px;\
            font-size: 17px !important;\
        \}\
        </style>\
        """, unsafe_allow_html=True)\
\
    st.caption("Local prototype \'b7 No account required")\
\
\
# --------------------------------------------------\
# SLIDE 1: HOME / LANDING PAGE\
# --------------------------------------------------\
\
if page == "Home":\
    st.markdown("""\
    <section class="hero">\
        <span class="kicker">SMART MEDICINE CARE</span>\
        <h1>CARE THAT<br>REMEMBERS<br>EVERY DOSE.</h1>\
        <p>Thoughtful reminders. Safer routines. Better adherence.</p>\
    </section>\
    """, unsafe_allow_html=True)\
\
    st.write("")\
\
    cards = [\
        (\
            "01",\
            "Medicine reminders",\
            "Keep your schedule close with a clear daily dose history."\
        ),\
        (\
            "02",\
            "Adherence insights",\
            "Understand weekly progress through simple visual reports."\
        ),\
        (\
            "03",\
            "AI risk explanation",\
            "Explore the reasons behind a demonstration risk result."\
        )\
    ]\
\
    columns = st.columns(3)\
    for col, (number, title, description) in zip(columns, cards):\
        with col:\
            st.markdown(f"""\
            <div class="slide-card">\
                <div class="slide-number">FEATURE \{number\}</div>\
                <h3>\{title\}</h3>\
                <p>\{description\}</p>\
            </div>\
            """, unsafe_allow_html=True)\
\
    st.write("")\
    left, center, right = st.columns([1, 2, 1])\
\
    with center:\
        st.markdown(\
            "<p style='text-align:center;color:#806B5C'>"\
            "A calmer, clearer way to manage your daily medicine routine."\
            "</p>",\
            unsafe_allow_html=True\
        )\
\
        if st.button("OPEN YOUR DASHBOARD  \uc0\u8594 ", type="primary",\
                     use_container_width=True):\
            st.session_state["navigate_dashboard"] = True\
            st.rerun()\
\
    st.markdown("---")\
    st.subheader("Designed around thoughtful care")\
    st.write(\
        "A warm, accessible interface for reminders, adherence tracking "\
        "and educational AI demonstrations."\
    )\
\
\
# --------------------------------------------------\
# SLIDE 2: DASHBOARD\
# --------------------------------------------------\
\
elif page == "Dashboard":\
    st.title("Your daily dashboard")\
    st.caption(datetime.now().strftime("%A, %d %B %Y"))\
\
    medicines = read_table("medicines")\
    logs = read_table("logs")\
\
    today_logs = (\
        logs[logs["scheduled_date"] == date.today().isoformat()]\
        if not logs.empty else pd.DataFrame()\
    )\
\
    taken = (\
        int((today_logs["status"] == "Taken").sum())\
        if not today_logs.empty else 0\
    )\
    missed = (\
        int((today_logs["status"] == "Missed").sum())\
        if not today_logs.empty else 0\
    )\
\
    a, b, c, d = st.columns(4)\
\
    with a:\
        show_metric("Medicines", len(medicines), "in your cabinet")\
    with b:\
        show_metric("Taken today", taken, "logged entries")\
    with c:\
        show_metric("Missed today", missed, "logged entries")\
    with d:\
        next_time = (\
            medicines["schedule"].min()\
            if not medicines.empty else "\'97"\
        )\
        show_metric("Next scheduled time", next_time, "earliest saved time")\
\
    st.write("")\
    st.subheader("Today's medicine list")\
\
    if medicines.empty:\
        st.info("Your cabinet is empty. Add a medicine to begin.")\
    else:\
        for _, medicine in medicines.sort_values("schedule").iterrows():\
            with st.container(border=True):\
                x, y, z = st.columns([3, 2, 2])\
\
                x.markdown(f"### \{medicine['name']\}")\
                x.write(medicine["dose"] or "Dose instructions not added.")\
                y.write(f"**Time:** \{medicine['schedule']\}")\
                z.write(f"**Stock:** \{medicine['stock']\}")\
\
                col1, col2 = st.columns(2)\
\
                if col1.button(\
                    "\uc0\u10003  Taken",\
                    key=f"taken_\{medicine['id']\}_\{datetime.now().date()\}"\
                ):\
                    record_dose(medicine, "Taken")\
                    st.success("Dose marked as Taken.")\
                    st.rerun()\
\
                if col2.button(\
                    "Missed",\
                    key=f"missed_\{medicine['id']\}_\{datetime.now().date()\}"\
                ):\
                    record_dose(medicine, "Missed")\
                    st.warning("Dose marked as Missed.")\
                    st.rerun()\
\
    st.subheader("Recent dose history")\
    if logs.empty:\
        st.caption("Your dose history will appear here.")\
    else:\
        st.dataframe(\
            logs.sort_values("logged_at", ascending=False).head(15),\
            use_container_width=True,\
            hide_index=True\
        )\
\
\
# --------------------------------------------------\
# MEDICINE CABINET\
# --------------------------------------------------\
\
elif page == "Medicine Cabinet":\
    st.title("Medicine cabinet")\
\
    with st.form("add_medicine", clear_on_submit=True):\
        name = st.text_input("Medicine name")\
        dose = st.text_input(\
            "Dose / instructions",\
            placeholder="As prescribed by your clinician"\
        )\
        schedule = st.time_input("Daily reminder time", value=time(9, 0))\
        stock = st.number_input(\
            "Stock units", min_value=0, max_value=10000, value=10\
        )\
        contact = st.text_input("Support contact (optional)")\
        notes = st.text_area("Notes (optional)")\
\
        submitted = st.form_submit_button("Save medicine", type="primary")\
\
        if submitted:\
            if not name.strip():\
                st.error("Please enter a medicine name.")\
            else:\
                with get_db() as con:\
                    con.execute("""\
                        INSERT INTO medicines\
                        (name,dose,schedule,stock,contact,notes)\
                        VALUES (?,?,?,?,?,?)\
                    """, (\
                        name.strip(),\
                        dose.strip(),\
                        schedule.strftime("%H:%M"),\
                        int(stock),\
                        contact.strip(),\
                        notes.strip()\
                    ))\
\
                st.success("Medicine saved.")\
                st.rerun()\
\
    medicines = read_table("medicines")\
\
    if not medicines.empty:\
        st.subheader("Saved medicines")\
        st.dataframe(medicines, use_container_width=True, hide_index=True)\
\
        low_stock = medicines[medicines["stock"] <= 3]\
        if not low_stock.empty:\
            st.warning(\
                "Low stock: " + ", ".join(low_stock["name"].tolist())\
            )\
\
        selected_id = st.selectbox(\
            "Choose medicine to remove",\
            medicines["id"].tolist(),\
            format_func=lambda item_id: medicines.loc[\
                medicines["id"] == item_id, "name"\
            ].iloc[0]\
        )\
\
        if st.button("Delete selected medicine"):\
            with get_db() as con:\
                con.execute(\
                    "DELETE FROM medicines WHERE id=?",\
                    (int(selected_id),)\
                )\
            st.success("Medicine deleted.")\
            st.rerun()\
\
\
# --------------------------------------------------\
# SMART REMINDERS\
# --------------------------------------------------\
\
elif page == "Smart Reminders":\
    st.title("Smart medicine reminders")\
    st.caption(\
        "Schedules are checked while this page is open or refreshed. "\
        "This is not a background notification service."\
    )\
\
    medicines = read_table("medicines")\
    now = datetime.now()\
\
    st.markdown(f"### Local time: \{now.strftime('%H:%M:%S')\}")\
\
    if medicines.empty:\
        st.info("Add medicines in Medicine Cabinet first.")\
    else:\
        for _, medicine in medicines.iterrows():\
            scheduled = datetime.strptime(\
                medicine["schedule"], "%H:%M"\
            ).time()\
\
            st.markdown(f"#### \{medicine['name']\}")\
            st.write(f"Scheduled time: \{medicine['schedule']\}")\
\
            if now.time() >= scheduled:\
                st.warning(\
                    "The scheduled time has passed. Review your dose history."\
                )\
            else:\
                minutes = int((\
                    datetime.combine(date.today(), scheduled) - now\
                ).total_seconds() // 60)\
\
                st.info(f"Upcoming in approximately \{minutes\} minutes.")\
\
\
# --------------------------------------------------\
# SLIDE 3: AI RISK AND EXPLANATION\
# --------------------------------------------------\
\
elif page == "AI Risk & Explanation":\
    st.title("AI risk assessment")\
    st.warning(\
        "Educational demo only. This model uses synthetic data and is "\
        "not validated for clinical or medical decisions."\
    )\
\
    c1, c2 = st.columns(2)\
\
    with c1:\
        age = st.slider("Age", 18, 100, 55)\
        hour = st.slider("Usual medicine time (hour)", 0, 23, 9)\
\
    with c2:\
        missed_history = st.slider("Recent missed doses (demo)", 0, 14, 2)\
        reminder = st.selectbox("Reminder use", ["Yes", "No"])\
\
    sample = pd.DataFrame([\{\
        "hour": hour,\
        "age": age,\
        "missed_history": missed_history,\
        "reminder_used": int(reminder == "Yes")\
    \}])\
\
    risk_score = float(np.clip(regressor.predict(sample)[0], 0, 100))\
    risk_category = classifier.predict(sample)[0]\
\
    a, b = st.columns(2)\
\
    with a:\
        show_metric("Demo risk score", f"\{risk_score:.0f\}/100",\
                    "not a clinical score")\
    with b:\
        show_metric("Risk category", risk_category,\
                    "based on synthetic training data")\
\
    st.progress(int(risk_score))\
\
    st.subheader("Why this alert?")\
\
    reasons = []\
\
    if missed_history >= 3:\
        reasons.append(\
            f"Missed-dose history is elevated (\{missed_history\} in the demo input)."\
        )\
    if age >= 70:\
        reasons.append(\
            "Age 70+ contributes to this demonstration model's score."\
        )\
    if reminder == "No":\
        reasons.append(\
            "The selected input indicates reminders are not being used."\
        )\
    if hour < 7 or hour > 21:\
        reasons.append(\
            "The selected reminder hour is outside common daytime hours."\
        )\
    if not reasons:\
        reasons.append(\
            "No strong listed factors were selected; the model still "\
            "produces an estimate from synthetic data."\
        )\
\
    for reason in reasons:\
        st.write("\'95 " + reason)\
\
\
# --------------------------------------------------\
# SLIDE 4: PATTERN CLUSTERING\
# --------------------------------------------------\
\
elif page == "Pattern Clustering":\
    st.title("Medicine pattern clustering")\
    st.warning("Demonstration only; clusters are not medical categories.")\
\
    hour = st.slider("Typical medicine hour", 0, 23, 9)\
    misses = st.slider("Missed-dose count", 0, 10, 1)\
    reminder = st.selectbox("Reminder enabled?", ["Yes", "No"])\
\
    sample = pd.DataFrame([\{\
        "hour": hour,\
        "missed_history": misses,\
        "reminder_used": int(reminder == "Yes")\
    \}])\
\
    # The scaler and K-Means model both use these same three features.\
    cluster_id = int(\
        cluster_model.predict(cluster_scaler.transform(sample))[0]\
    )\
\
    st.markdown(f"### Pattern group \{cluster_id + 1\}")\
    st.write(\
        "This group reflects similarity in the demonstration dataset, "\
        "not a diagnosis or an individual prediction."\
    )\
\
    rng = np.random.default_rng(42)\
    plot_data = pd.DataFrame(\{\
        "Reminder hour": rng.integers(5, 24, 120),\
        "Missed doses": rng.integers(0, 9, 120),\
        "Group": rng.choice(\
            ["Group A", "Group B", "Group C"], 120\
        )\
    \})\
\
    fig = px.scatter(\
        plot_data,\
        x="Reminder hour",\
        y="Missed doses",\
        color="Group",\
        title="Illustrative medicine-taking patterns"\
    )\
    st.plotly_chart(fig, use_container_width=True)\
\
\
# --------------------------------------------------\
# MISSED-DOSE ESCALATION\
# --------------------------------------------------\
\
elif page == "Missed-dose Escalation":\
    st.title("Missed-dose follow-up")\
\
    logs = read_table("logs")\
    missed_logs = (\
        logs[logs["status"] == "Missed"]\
        if not logs.empty else pd.DataFrame()\
    )\
\
    count = len(missed_logs)\
\
    if count >= 5:\
        level = "High attention"\
    elif count >= 3:\
        level = "Follow-up suggested"\
    else:\
        level = "Routine"\
\
    st.markdown(f"### Status: \{level\}")\
    st.write(f"Recorded missed entries: **\{count\}**")\
\
    if count >= 3:\
        st.warning(\
            "Repeated missed entries found. Review the routine and "\
            "consider contacting the person's chosen support contact."\
        )\
\
        if st.button("Acknowledge follow-up"):\
            with get_db() as con:\
                con.execute("""\
                    INSERT INTO alerts (created_at,message,acknowledged)\
                    VALUES (?,?,1)\
                """, (\
                    datetime.now().isoformat(timespec="seconds"),\
                    "Follow-up acknowledged"\
                ))\
            st.success("Acknowledgement saved.")\
    else:\
        st.info("The demo follow-up suggestion appears after 3 missed entries.")\
\
    st.caption(\
        "This prototype does not send SMS, WhatsApp, emergency calls "\
        "or external contact notifications."\
    )\
\
    if not missed_logs.empty:\
        st.dataframe(missed_logs, use_container_width=True, hide_index=True)\
\
\
# --------------------------------------------------\
# VOICE REMINDER\
# --------------------------------------------------\
\
elif page == "Voice Reminder":\
    st.title("Voice reminder")\
\
    medicines = read_table("medicines")\
\
    if medicines.empty:\
        st.info("Add a medicine first.")\
    else:\
        medicine_name = st.selectbox(\
            "Choose a medicine", medicines["name"].tolist()\
        )\
\
        sentence = (\
            f"It is time to take your \{medicine_name\} medicine. "\
            "Please follow your prescribed instructions."\
        )\
\
        st.write("Reminder sentence:")\
        st.code(sentence)\
\
        st.caption(\
            "On macOS, the built-in speech command can read this sentence."\
        )\
\
        st.code(f"say \{repr(sentence)\}", language="bash")\
\
        st.caption(\
            "This command runs on your Mac when executed in Terminal; "\
            "it does not speak automatically when the website is closed."\
        )\
\
\
# --------------------------------------------------\
# MEDICINE PHOTO RECOGNITION DEMO\
# --------------------------------------------------\
\
elif page == "Medicine Recognition":\
    st.title("Medicine packaging photo")\
    st.warning(\
        "Visual similarity demo only. It cannot safely identify pills "\
        "or verify medicine authenticity."\
    )\
\
    st.write(\
        "Place reference packaging photos in the `medicine_images` "\
        "folder. Example filename: `VitaminD__reference.jpg`."\
    )\
\
    upload = st.file_uploader(\
        "Upload packaging photo", type=["png", "jpg", "jpeg"]\
    )\
\
    if upload:\
        image = Image.open(upload).convert("RGB")\
        st.image(image, caption="Uploaded photo", width=320)\
\
        candidates = []\
\
        for path in IMAGE_DIR.iterdir():\
            if path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:\
                continue\
\
            try:\
                reference = Image.open(path).convert("RGB").resize((32, 32))\
                uploaded_small = image.resize((32, 32))\
\
                a = np.asarray(uploaded_small, dtype=float)\
                b = np.asarray(reference, dtype=float)\
\
                distance = float(np.mean(np.abs(a - b)))\
                candidates.append((distance, path.name))\
            except Exception:\
                continue\
\
        if candidates:\
            distance, filename = min(candidates)\
            st.write(f"Closest reference image: **\{filename\}**")\
            st.write(f"Simple pixel distance: \{distance:.1f\}")\
        else:\
            st.info("No reference photos found in medicine_images.")\
\
        st.error(\
            "Do not use this result to decide which medicine to take. "\
            "Verify the packaging label and ask a pharmacist if unsure."\
        )\
\
\
# --------------------------------------------------\
# ELDER-FRIENDLY MODE\
# --------------------------------------------------\
\
elif page == "Elder-friendly Mode":\
    st.title("Simple medicine care")\
\
    st.markdown("""\
    <div style="\
        padding:28px;\
        border:2px solid #6D4A37;\
        border-radius:20px;\
        background:#FFFAF0;\
        color:#4B3024;\
    ">\
        <div style="font-family:'Bodoni Moda',serif;font-size:34px">\
            Your medicine routine\
        </div>\
        <p style="font-size:22px">\
            Check your medicine name and the instructions on its label.\
        </p>\
        <p style="font-size:18px">\
            1. Check the scheduled time.<br>\
            2. Follow your prescribed instructions.<br>\
            3. Record the dose after taking it.\
        </p>\
    </div>\
    """, unsafe_allow_html=True)\
\
    st.caption("Use the sidebar toggle to enlarge text and controls.")\
\
\
# --------------------------------------------------\
# ADHERENCE REPORTS\
# --------------------------------------------------\
\
elif page == "Adherence Reports":\
    st.title("Adherence reports")\
\
    logs = read_table("logs")\
\
    if logs.empty:\
        st.info(\
            "Mark doses Taken or Missed on the Dashboard to create a report."\
        )\
    else:\
        logs["scheduled_date"] = pd.to_datetime(\
            logs["scheduled_date"], errors="coerce"\
        )\
\
        logs["week"] = (\
            logs["scheduled_date"]\
            .dt.to_period("W")\
            .astype(str)\
        )\
\
        weekly = logs.groupby("week").agg(\
            total=("status", "count"),\
            taken=("status", lambda values: (values == "Taken").sum())\
        ).reset_index()\
\
        weekly["adherence_pct"] = (\
            weekly["taken"] / weekly["total"] * 100\
        ).round(1)\
\
        latest = weekly.iloc[-1]\
\
        show_metric(\
            "Latest logged week",\
            f"\{latest['adherence_pct']:.1f\}%",\
            "manually logged doses marked Taken"\
        )\
\
        fig = px.bar(\
            weekly,\
            x="week",\
            y="adherence_pct",\
            range_y=[0, 100],\
            labels=\{\
                "week": "Week",\
                "adherence_pct": "Adherence (%)"\
            \},\
            title="Weekly adherence percentage"\
        )\
\
        st.plotly_chart(fig, use_container_width=True)\
        st.dataframe(weekly, use_container_width=True, hide_index=True)\
\
        st.download_button(\
            "Download dose history CSV",\
            data=logs.to_csv(index=False).encode("utf-8"),\
            file_name="jeevan_kavach_adherence.csv",\
            mime="text/csv"\
        )\
\
    st.caption(\
        "This percentage is based only on records manually entered in the app."\
    )\
\
\
# --------------------------------------------------\
# FOOTER\
# --------------------------------------------------\
\
st.markdown("---")\
st.markdown("""\
<p style="\
    text-align:center;\
    color:#806B5C;\
    font-size:12px;\
    letter-spacing:2px;\
    padding:12px;\
">\
JEEVAN KAVACH \'b7 THOUGHTFUL REMINDERS, SAFER ROUTINES\
</p>\
""", unsafe_allow_html=True)\
}
