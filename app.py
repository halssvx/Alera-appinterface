import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Alera – Diabetes Companion",
    page_icon="💚",
    layout="wide",
)

# ---------- STATE INITIALISATION ----------
def init_state():
    if "settings" not in st.session_state:
        st.session_state.settings = {
            "diabetes_type": "Type 1",
            "target_min": 4.0,
            "target_max": 10.0,
            "hypo_threshold": 4.0,
            "hyper_threshold": 14.0,
        }
    if "bg_readings" not in st.session_state:
        st.session_state.bg_readings: List[Dict[str, Any]] = []
    if "med_logs" not in st.session_state:
        st.session_state.med_logs: List[Dict[str, Any]] = []
    if "meal_logs" not in st.session_state:
        st.session_state.meal_logs: List[Dict[str, Any]] = []
    if "activity_logs" not in st.session_state:
        st.session_state.activity_logs: List[Dict[str, Any]] = []

init_state()

settings = st.session_state.settings
bg_readings = st.session_state.bg_readings
med_logs = st.session_state.med_logs
meal_logs = st.session_state.meal_logs
activity_logs = st.session_state.activity_logs

# ---------- HELPERS (DATAFRAMES) ----------
def bg_df() -> pd.DataFrame:
    if not bg_readings:
        return pd.DataFrame(columns=["time", "value", "context", "notes"])
    df = pd.DataFrame(bg_readings)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    return df.sort_values("time")

def med_df() -> pd.DataFrame:
    if not med_logs:
        return pd.DataFrame(columns=["time", "name", "dose", "taken"])
    df = pd.DataFrame(med_logs)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    return df.sort_values("time")

def meal_df() -> pd.DataFrame:
    if not meal_logs:
        return pd.DataFrame(columns=["time", "description", "carbs"])
    df = pd.DataFrame(meal_logs)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    return df.sort_values("time")

def activity_df() -> pd.DataFrame:
    if not activity_logs:
        return pd.DataFrame(columns=["time", "type", "duration", "intensity"])
    df = pd.DataFrame(activity_logs)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    return df.sort_values("time")

# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.title("💚 Alera")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Log blood glucose",
        "Medication",
        "Food",
        "Activity",
        "Insights",
        "Education & coping",
        "Settings",
    ],
)

st.sidebar.markdown(
    "This app is a **support tool** and does **not** replace your diabetes team."
)

# ---------- EMERGENCY BANNER ----------
_all_bg = bg_df()
latest_bg = _all_bg.iloc[-1] if not _all_bg.empty else None

if latest_bg is not None:
    if latest_bg["value"] < settings["hypo_threshold"]:
        st.warning(
            "⚠️ **Low blood sugar alert**  \n"
            f"Your latest reading is **{latest_bg['value']} mmol/L**, "
            "which is below your low threshold. "
            "Take fast-acting sugar (e.g. juice or glucose tablets), "
            "re-check in about 15 minutes, and contact emergency services "
            "or your healthcare team if you feel very unwell.",
            icon="⚠️",
        )
    elif latest_bg["value"] > settings["hyper_threshold"]:
        st.error(
            "🚨 **High blood sugar alert**  \n"
            f"Your latest reading is **{latest_bg['value']} mmol/L**, "
            "which is above your high threshold. If you feel very unwell "
            "(nausea, vomiting, tummy pain, deep breathing), contact "
            "emergency services or your healthcare team urgently.",
            icon="🚨",
        )

# ---------- PAGES ----------
def page_dashboard():
    st.title("📊 Dashboard")

    df_all = bg_df()

    col1, col2 = st.columns([1.2, 1])

    # --- LEFT: Latest + chart ---
    with col1:
        st.subheader("Latest reading")

        latest = df_all.iloc[-1] if not df_all.empty else None

        if latest is None:
            st.info("No readings yet – log your first reading on the *Log blood glucose* page.")
        else:
            st.markdown(
                f"""
                <div style="
                    padding: 1rem;
                    border-radius: 1rem;
                    border: 1px solid rgba(148,163,184,0.5);
                    background: rgba(15,23,42,0.85);
                ">
                  <div style="font-size: 2.2rem; font-weight: 700; color: #22c55e;">
                    {latest['value']} <span style="font-size: 1rem; color: #9ca3af;">mmol/L</span>
                  </div>
                  <div style="font-size: 0.85rem; color: #9ca3af;">
                    {latest['time'].strftime('%d %b %Y, %H:%M')} · {latest['context']}
                  </div>
                  <div style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.15rem;">
                    Target: {settings['target_min']} – {settings['target_max']} mmol/L
                  </div>
                  {"<div style='margin-top:0.35rem; font-size:0.85rem; color:#e5e7eb;'>“" + str(latest['notes']) + "”</div>" if pd.notna(latest['notes']) and latest['notes'] else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### Trend over time")
        if df_all.empty:
            st.info("Once you add some readings, a chart will appear here.")
        else:
            chart_df = df_all.set_index("time")[["value"]]
            st.line_chart(chart_df)

    # --- RIGHT: Today & counts ---
    with col2:
        st.subheader("Today at a glance")

        today = pd.Timestamp.today().normalize()

        def today_filter(df: pd.DataFrame) -> pd.DataFrame:
            if df.empty:
                return df
            times = pd.to_datetime(df["time"], errors="coerce")
            return df[times.dt.normalize() == today]

        df_bg_today = today_filter(df_all)
        df_med_today = today_filter(med_df())
        df_meal_today = today_filter(meal_df())
        df_act_today = today_filter(activity_df())

        def stat(label: str, value: Any):
            st.markdown(
                f"""
                <div style="
                    padding: 0.4rem 0.7rem;
                    margin-bottom: 0.3rem;
                    border-radius: 999px;
                    border: 1px solid rgba(148,163,184,0.6);
                    display: flex;
                    justify-content: space-between;
                    font-size: 0.85rem;
                ">
                  <span style="color:#9ca3af;">{label}</span>
                  <span style="font-weight:600;">{value}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        stat("Readings today", len(df_bg_today))
        stat("Meds logged today", len(df_med_today))
        stat("Meals today", len(df_meal_today))
        stat("Activity logs today", len(df_act_today))

        total = len(df_all)
        if total:
            in_range = df_all[
                (df_all["value"] >= settings["target_min"])
                & (df_all["value"] <= settings["target_max"])
            ]
            lows = df_all[df_all["value"] < settings["hypo_threshold"]]
            highs = df_all[df_all["value"] > settings["hyper_threshold"]]
            stat("Total readings", total)
            stat("In range (%)", f"{round(len(in_range) / total * 100)}%")
            stat("Lows", len(lows))
            stat("Highs", len(highs))
        else:
            st.caption("Log some readings to see more stats here.")

def page_log_bg():
    st.title("🩸 Log blood glucose")

    with st.form("bg_form", clear_on_submit=True):
        cols = st.columns(2)
        with cols[0]:
            value = st.number_input("Value (mmol/L)", min_value=0.0, step=0.1)
            context = st.selectbox(
                "Context",
                ["Before meal", "After meal", "Waking", "Bedtime", "Exercise"],
            )
        with cols[1]:
            # Date + time instead of st.datetime_input
            date_input = st.date_input("Date", value=datetime.now().date())
            time_input = st.time_input("Time", value=datetime.now().time())
            time = datetime.combine(date_input, time_input)

            notes = st.text_input(
                "Notes (optional)",
                placeholder="How you felt / what was happening",
            )

        submitted = st.form_submit_button("Save reading")
        if submitted:
            bg_readings.append(
                {
                    "time": time.isoformat(),
                    "value": float(value),
                    "context": context,
                    "notes": notes.strip(),
                }
            )
            st.success("Saved blood glucose reading ✅")

    st.markdown("### Recent readings")
    df = bg_df().tail(15)
    if df.empty:
        st.info("No readings yet.")
    else:
        df_display = df.copy()
        df_display["time"] = df_display["time"].dt.strftime("%d %b %Y, %H:%M")
        st.dataframe(df_display, use_container_width=True)

def page_meds():
    st.title("💊 Medication")

    with st.form("med_form", clear_on_submit=True):
        cols = st.columns(2)
        with cols[0]:
            name = st.text_input(
                "Medication name",
                placeholder="e.g. Metformin, long-acting insulin",
            )
            dose = st.text_input("Dose", placeholder="e.g. 500mg, 10 units")
        with cols[1]:
            # Date + time instead of st.datetime_input
            date_input = st.date_input("Date (medication)", value=datetime.now().date())
            time_input = st.time_input("Time (medication)", value=datetime.now().time())
            time = datetime.combine(date_input, time_input)

            taken = st.checkbox("Taken now", value=True)

        submitted = st.form_submit_button("Save medication log")
        if submitted:
            if not name.strip():
                st.error("Please enter a medication name.")
            else:
                med_logs.append(
                    {
                        "time": time.isoformat(),
                        "name": name.strip(),
                        "dose": dose.strip() or "As prescribed",
                        "taken": bool(taken),
                    }
                )
                st.success("Saved medication log ✅")

    st.markdown("### Recent medication")
    df = med_df().tail(20)
    if df.empty:
        st.info("No medication logged yet.")
    else:
        df_display = df.copy()
        df_display["time"] = df_display["time"].dt.strftime("%d %b %Y, %H:%M")
        df_display["taken"] = df_display["taken"].map(
            {True: "Taken", False: "Missed"}
        )
        st.dataframe(df_display, use_container_width=True)

def page_food():
    st.title("🍽️ Food & carbs")

    with st.form("meal_form", clear_on_submit=True):
        description = st.text_input(
            "Meal / snack", placeholder="e.g. rice and chicken, porridge"
        )
        cols = st.columns(2)
        with cols[0]:
            carbs = st.number_input(
                "Carbs (g, optional)", min_value=0, step=1
            )
        with cols[1]:
            # Date + time instead of st.datetime_input
            date_input = st.date_input("Date (meal)", value=datetime.now().date())
            time_input = st.time_input("Time (meal)", value=datetime.now().time())
            time = datetime.combine(date_input, time_input)

        submitted = st.form_submit_button("Save meal")
        if submitted:
            if not description.strip():
                st.error("Please enter a description.")
            else:
                meal_logs.append(
                    {
                        "time": time.isoformat(),
                        "description": description.strip(),
                        "carbs": int(carbs) if carbs else None,
                    }
                )
                st.success("Saved meal ✅")

    st.markdown("### Recent meals")
    df = meal_df().tail(20)
    if df.empty:
        st.info("No meals logged yet.")
    else:
        df_display = df.copy()
        df_display["time"] = df_display["time"].dt.strftime("%d %b %Y, %H:%M")
        st.dataframe(df_display, use_container_width=True)

def page_activity():
    st.title("🏃 Activity")

    with st.form("activity_form", clear_on_submit=True):
        type_ = st.text_input(
            "Activity type",
            placeholder="e.g. walking, football, gym",
        )
        cols = st.columns(2)
        with cols[0]:
            duration = st.number_input(
                "Duration (minutes)", min_value=0, step=5
            )
        with cols[1]:
            intensity = st.selectbox(
                "Intensity", ["Light", "Moderate", "Intense"]
            )

        # Date + time instead of st.datetime_input
        date_input = st.date_input("Date (activity)", value=datetime.now().date())
        time_input = st.time_input("Time (activity)", value=datetime.now().time())
        time = datetime.combine(date_input, time_input)

        submitted = st.form_submit_button("Save activity")
        if submitted:
            if not type_.strip():
                st.error("Please enter an activity.")
            else:
                activity_logs.append(
                    {
                        "time": time.isoformat(),
                        "type": type_.strip(),
                        "duration": int(duration),
                        "intensity": intensity,
                    }
                )
                st.success("Saved activity ✅")

    st.markdown("### Recent activity")
    df = activity_df().tail(20)
    if df.empty:
        st.info("No activity logged yet.")
    else:
        df_display = df.copy()
        df_display["time"] = df_display["time"].dt.strftime("%d %b %Y, %H:%M")
        st.dataframe(df_display, use_container_width=True)

def page_insights():
    st.title("🧠 Insights & patterns")

    df = bg_df()
    if df.empty:
        st.info("Once you’ve logged some readings, insights will appear here.")
        return

    insights = []

    lows = df[df["value"] < settings["hypo_threshold"]]
    highs = df[df["value"] > settings["hyper_threshold"]]
    in_range = df[
        (df["value"] >= settings["target_min"])
        & (df["value"] <= settings["target_max"])
    ]

    if len(lows) >= 3:
        insights.append(
            "You’ve had several low readings. This is something to discuss with your "
            "diabetes nurse or doctor. Make sure you carry fast-acting sugar with you."
        )
    if len(highs) >= 3:
        insights.append(
            "You’ve had multiple high readings. It may help to review your insulin/"
            "medication and meal pattern with your healthcare team."
        )
    if len(df) >= 5 and len(in_range) / len(df) >= 0.7:
        insights.append(
            "A lot of your readings are within your target range. That’s really positive – "
            "remember that one off day doesn’t mean failure."
        )
    if not insights:
        insights.append(
            "Your readings are still building up. Keep logging and patterns will become "
            "clearer to talk through with your team."
        )

    st.markdown("### Suggestions based on your data")
    for i, text in enumerate(insights, start=1):
        st.markdown(f"**Insight {i}:** {text}")

    st.markdown("### Graph view")
    chart_df = df.set_index("time")[["value"]]
    st.line_chart(chart_df)

    st.caption(
        "This app never tells you to change your doses. It only highlights patterns so you can "
        "discuss them with a professional."
    )

def page_education():
    st.title("📚 Education & coping")

    st.markdown(
        """
        Living with diabetes means juggling food, movement, stress, sleep, and medication.  
        This space is for calm, human-language explanations – not judgement.
        """
    )

    with st.expander("Lows (hypoglycaemia)"):
        st.write(
            "Low blood sugar can make you feel shaky, sweaty, confused, hungry, or just 'not right'. "
            "Treat with fast-acting sugar (like juice or glucose tablets) and re-test after about "
            "15 minutes. If you don’t feel better, or you can’t keep sugar down, seek urgent "
            "medical help."
        )

    with st.expander("Highs (hyperglycaemia)"):
        st.write(
            "High blood sugar over time can cause complications, but one high reading does **not** "
            "mean you’ve failed. If you have very high readings and feel very unwell "
            "(tummy pain, sickness, heavy breathing), contact emergency services – especially if you use insulin."
        )

    with st.expander("Stress, sleep & emotions"):
        st.write(
            "Exams, arguments, poor sleep and illness can all push your numbers up or down. You are "
            "not a robot. Some days will just be messy – and that’s okay. What matters is safety "
            "and patterns over time, not perfection."
        )

    with st.expander("Talking to your diabetes team"):
        st.write(
            "Bring this app to appointments. Show your nurse or doctor your readings and notes. "
            "Use phrases like *'I’ve noticed I’m often high in the morning'* instead of *'I’m bad at this'*. "
            "You deserve care, not judgement."
        )

    st.caption(
        "Always follow advice from your diabetes team. This app is a companion, not a replacement for professional care."
    )

def page_settings():
    st.title("⚙️ Settings")

    st.markdown("Set targets **with your healthcare team** if you can.")

    with st.form("settings_form"):
        diabetes_type = st.selectbox(
            "Diabetes type",
            ["Type 1", "Type 2", "Gestational", "Other / unsure"],
            index=["Type 1", "Type 2", "Gestational", "Other / unsure"].index(
                settings["diabetes_type"]
            )
            if settings["diabetes_type"]
            in ["Type 1", "Type 2", "Gestational", "Other / unsure"]
            else 0,
        )

        col1, col2 = st.columns(2)
        with col1:
            target_min = st.number_input(
                "Target min (mmol/L)",
                value=float(settings["target_min"]),
                step=0.1,
            )
            hypo_threshold = st.number_input(
                "Low alert threshold",
                value=float(settings["hypo_threshold"]),
                step=0.1,
            )
        with col2:
            target_max = st.number_input(
                "Target max (mmol/L)",
                value=float(settings["target_max"]),
                step=0.1,
            )
            hyper_threshold = st.number_input(
                "High alert threshold",
                value=float(settings["hyper_threshold"]),
                step=0.1,
            )

        submitted = st.form_submit_button("Save settings")
        if submitted:
            settings["diabetes_type"] = diabetes_type
            settings["target_min"] = float(target_min)
            settings["target_max"] = float(target_max)
            settings["hypo_threshold"] = float(hypo_threshold)
            settings["hyper_threshold"] = float(hyper_threshold)
            st.success("Settings updated ✅")

    st.caption(
        "These values are used to colour readings as low / in range / high and to show safety alerts."
    )

# ---------- ROUTER ----------
if page == "Dashboard":
    page_dashboard()
elif page == "Log blood glucose":
    page_log_bg()
elif page == "Medication":
    page_meds()
elif page == "Food":
    page_food()
elif page == "Activity":
    page_activity()
elif page == "Insights":
    page_insights()
elif page == "Education & coping":
    page_education()
elif page == "Settings":
    page_settings()
