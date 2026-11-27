import streamlit as st
import time
import math
from database import get_quests, update_quest, delete_quest, add_quest, user_auth, get_xp, get_connection, get_task_stats, get_today_tasks
from datetime import date, timedelta
import json
from pathlib import Path
from database import *
import sqlite3
import datetime


st.set_page_config(layout="wide")

if "user" not in st.session_state or not st.session_state.user.get("logged_in"):
    st.warning("Please log in on the Home page first.")
    st.stop()

userid = st.session_state.user.get("user_id")
current_xp = get_xp(userid)


# ---------------- LEVEL SYSTEM ----------------

def level_details(xp):
    levels = [
        ("Beginner", 0, 100),
        ("Learner", 100, 300),
        ("Achiever", 300, 600),
        ("Expert", 600, 1000),
        ("Master", 1000, 1500),
        ("Legend", 1500, None)
    ]

    for level, start, end in levels:

        if end is None or xp < end:

            if end is None:
                progress = 100
                remaining = 0

            else:
                progress = int(
                    (xp - start) / (end - start) * 100
                )
                remaining = end - xp

            return level, progress, remaining, end

    return "Legend", 100, 0, None


# ---------------- BADGES ----------------

def get_badges(xp, total_tasks):
    return [
        ("🌱 First Step", total_tasks >= 1, "Complete your first task"),
        ("📚 Task Master", total_tasks >= 10, "Complete 10 tasks"),
        ("⭐ XP Hunter", xp >= 500, "Earn 500 XP"),
        ("💎 XP Champion", xp >= 1000, "Earn 1,000 XP"),
    ]

# ---------------- CSS ----------------

def load_css(file_name):
    css_path = Path(__file__).parent.parent / file_name

    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    else:
        st.error(f"CSS file '{file_name}' not found.")


load_css("styles.css")
# ---------------- MASTER TABS ----------------


# ---------------- PRODUCTIVITY DASHBOARD ----------------

total_tasks, completed_tasks = get_task_stats(userid)
level_name, level_progress, xp_to_next, next_level_xp = level_details(current_xp)
badges = get_badges(current_xp, completed_tasks)
earned_badges = sum(1 for _, earned, _ in badges if earned)

st.title("My Productive Zone")

st.caption(
    "Your study progress, XP, streaks and achievements — "
    "all in one place."
)

# ---------------- SUMMARY CARDS ----------------

c1, c3, c4 = st.columns(3)

with c1:
    with st.container(border=True):
        st.metric(
            "⭐ Total XP", current_xp,
            help="Total Experience Points earned by completing tasks.")

with c3:
    with st.container(border=True):
        st.metric(
            "🏅 Current Level",
            level_name,
            help="Your current level based on the XP you have earned."
        )

with c4:
    with st.container(border=True):
        st.metric(
            "🎖️ Badges Earned",
            f"{earned_badges}/8",
            help="The number of achievement badges you have unlocked so far."
        )


with st.container(border=True):

    today_tasks, today_completed_tasks = get_today_tasks(userid)

    st.subheader("🗓️ Daily Stats")
    d1, d2, d3= st.columns(3)

    with d1:
        st.metric("💠 Total Tasks Today", today_tasks, border=True, help="Total number of tasks today", width="content")

    with d2:
        st.metric("☑️ Tasks Completed Today", today_completed_tasks, border=True, help="Number of tasks completed today", width="content")

    with d3:
        st.metric("✨ XP Earned Today", today_completed_tasks*20, border=True, help="XP you earned by completing today's tasks", width="content")





# ---------------- LEVEL PROGRESS ----------------

with st.container(border=True):

    st.subheader(
        f"Level Progress — {level_name}"
    )

    if next_level_xp is None:

        st.success(
            "You've reached the highest level: Legend!"
        )

    else:

        st.progress(level_progress / 100)

        st.caption(
            f"{current_xp} XP total · "
            f"{xp_to_next} XP to the next level"
        )

# ---------------- ACHIEVEMENTS ----------------

with st.container(border=True):

    st.subheader("🎖️ Achievements & Badges")

    badge_columns = st.columns(4)

    for index, (
            badge_name,
            earned,
            requirement
    ) in enumerate(get_badges(current_xp, total_tasks)):

        with badge_columns[index % 4]:

            if earned:

                st.success(badge_name)
                st.caption("Unlocked!")

            else:

                st.info(f"🔒 {badge_name}")
                st.caption(requirement)


