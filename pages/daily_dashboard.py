import streamlit as st
import time
import math
from database import get_quests, update_quest, delete_quest
from database import add_quest, user_auth
from pathlib import Path
from datetime import date, timedelta
import json
from database import *

st.set_page_config(layout="wide")

if "user" not in st.session_state or not st.session_state.user.get("logged_in"):
    st.warning("Please log in on the Home page first.")
    st.stop()

# ---------------- PRODUCTIVITY DATA ----------------

DATA_FILE = Path(__file__).parent.parent / "productivity_data.json"


def empty_productivity_data():
    return {
        "xp": 0,
        "awarded_task_ids": [],
        "five_task_bonus_days": [],
        "all_tasks_bonus_days": [],
        "perfect_days": [],
        "daily_stats": {},
        "xp_sources": {
            "Task XP": 0,
            "Daily bonuses": 0,
            "Focus sessions": 0
        }
    }


def load_productivity_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                saved = json.load(file)

            defaults = empty_productivity_data()
            defaults.update(saved)

            # Safely merge XP sources so older saved files still work.
            saved_sources = saved.get("xp_sources", {})
            defaults["xp_sources"] = {
                key: saved_sources.get(key, value)
                for key, value in defaults["xp_sources"].items()
            }

            return defaults

        except (json.JSONDecodeError, OSError, TypeError):
            return empty_productivity_data()

    return empty_productivity_data()


st.session_state.productivity_data = load_productivity_data()


def save_productivity_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            st.session_state.productivity_data,
            file,
            indent=4
        )


def today_key():
    return date.today().isoformat()


def get_today_stats():
    data = st.session_state.productivity_data
    key = today_key()

    if key not in data["daily_stats"]:
        data["daily_stats"][key] = {
            "tasks": 0,
            "focus_sessions": 0,
            "study_minutes": 0,
            "xp": 0
        }

    return data["daily_stats"][key]


# ---------------- XP SYSTEM ----------------

def add_xp(points, source):
    data = st.session_state.productivity_data

    data["xp"] += points
    data["xp_sources"][source] += points
    get_today_stats()["xp"] += points

    save_productivity_data()


def award_task_xp(task_id):
    data = st.session_state.productivity_data
    task_id = str(task_id)

    # A task can award XP only once.
    if task_id in data["awarded_task_ids"]:
        return

    priority_points = {
        "Low": 5,
        "Moderate": 10,
        "High": 20
    }

    priority = st.session_state.get(
        f"priority_{task_id}",
        "Moderate"
    )

    points = priority_points.get(priority, 10)

    data["awarded_task_ids"].append(task_id)
    get_today_stats()["tasks"] += 1

    add_xp(points, "Task XP")

    # Bonus for completing 5 tasks in one day.
    day = today_key()

    if (
            get_today_stats()["tasks"] >= 5
            and day not in data["five_task_bonus_days"]
    ):
        data["five_task_bonus_days"].append(day)

        add_xp(15, "Daily bonuses")

        st.toast(
            "5 tasks completed! +15 bonus XP 🎉",
            icon="⭐"
        )


def award_all_tasks_bonus():
    data = st.session_state.productivity_data
    day = today_key()

    if day not in data["all_tasks_bonus_days"]:
        data["all_tasks_bonus_days"].append(day)
        data["perfect_days"].append(day)

        add_xp(20, "Daily bonuses")

        st.toast(
            "All your tasks are complete! +20 bonus XP 🎉",
            icon="🏆"
        )


def record_focus_session():
    data = st.session_state.productivity_data
    stats = get_today_stats()

    stats["focus_sessions"] += 1
    stats["study_minutes"] += int(
        st.session_state.get("study_minutes", 0)
    )

    add_xp(10, "Focus sessions")

    st.toast(
        "Focus session completed! +10 XP 🎯",
        icon="⏱️"
    )


# ---------------- STREAK SYSTEM ----------------

def productivity_streaks():
    stats = st.session_state.productivity_data["daily_stats"]
    productive_days = []

    for day, values in stats.items():
        if (
                values.get("tasks", 0) >= 3
                or values.get("focus_sessions", 0) >= 1
        ):
            productive_days.append(date.fromisoformat(day))

    productive_days = sorted(set(productive_days))

    if not productive_days:
        return 0, 0

    # Best-ever streak
    best = 1
    run = 1

    for previous, current in zip(
            productive_days,
            productive_days[1:]
    ):
        if current == previous + timedelta(days=1):
            run += 1
        else:
            run = 1

        best = max(best, run)

    # Current streak
    productive_set = set(productive_days)

    if date.today() in productive_set:
        cursor = date.today()
    else:
        cursor = date.today() - timedelta(days=1)

    current = 0

    while cursor in productive_set:
        current += 1
        cursor -= timedelta(days=1)

    return current, best


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

    for name, start, end in levels:

        if end is None or xp < end:

            if end is None:
                progress = 100
                remaining = 0

            else:
                progress = int(
                    (xp - start) / (end - start) * 100
                )
                remaining = end - xp

            return name, progress, remaining, end

    return "Legend", 100, 0, None


# ---------------- BADGES ----------------

def get_badges():
    data = st.session_state.productivity_data
    stats = data["daily_stats"]

    total_tasks = sum(
        day.get("tasks", 0)
        for day in stats.values()
    )

    total_focus = sum(
        day.get("focus_sessions", 0)
        for day in stats.values()
    )

    current_streak, best_streak = productivity_streaks()
    xp = data["xp"]

    badge_rules = [
        (
            "🌱 First Step",
            total_tasks >= 1,
            "Complete your first task"
        ),
        (
            "📚 Task Master",
            total_tasks >= 10,
            "Complete 10 tasks"
        ),
        (
            "🔥 Focus Freak",
            total_focus >= 10,
            "Complete 10 focus sessions"
        ),
        (
            "⭐ XP Hunter",
            xp >= 500,
            "Earn 500 XP"
        ),
        (
            "💎 XP Champion",
            xp >= 1000,
            "Earn 1,000 XP"
        ),
        (
            "🔥 Weekly Warrior",
            best_streak >= 7,
            "Build a 7-day streak"
        ),
        (
            "👑 Consistency King",
            best_streak >= 30,
            "Build a 30-day streak"
        ),
        (
            "🎯 Perfect Day",
            len(data["perfect_days"]) >= 1,
            "Complete all tasks in a day"
        )
    ]

    return badge_rules


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

# IMPORTANT FIX:
# st.tabs() returns a list, so unpack the single tab using a comma.

t0, = st.tabs([
    "📊 Productivity Dashboard"
])

# ---------------- PRODUCTIVITY DASHBOARD ----------------

with t0:
    st.title("My Productive Zone")

    st.caption(
        "Your study progress, XP, streaks and achievements — "
        "all in one place."
    )

    data = st.session_state.productivity_data

    today_stats = get_today_stats()

    current_streak, best_streak = productivity_streaks()

    level_name, level_progress, xp_to_next, next_level_xp = (
        level_details(data["xp"])
    )

    total_tasks_completed = sum(
        day.get("tasks", 0)
        for day in data["daily_stats"].values()
    )

    total_focus_sessions = sum(
        day.get("focus_sessions", 0)
        for day in data["daily_stats"].values()
    )

    total_study_minutes = sum(
        day.get("study_minutes", 0)
        for day in data["daily_stats"].values()
    )

    earned_badges = sum(
        1
        for _, earned, _ in get_badges()
        if earned
    )

    # ---------------- SUMMARY CARDS ----------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        with st.container(border=True):
            st.metric("⭐ Total XP", data["xp"])

    with c2:
        with st.container(border=True):
            st.metric(
                "🔥 Current Streak",
                f"{current_streak} days"
            )

    with c3:
        with st.container(border=True):
            st.metric(
                "🏅 Current Level",
                level_name
            )

    with c4:
        with st.container(border=True):
            st.metric(
                "🎖️ Badges Earned",
                f"{earned_badges}/8"
            )

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
                f"{data['xp']} XP total · "
                f"{xp_to_next} XP to the next level"
            )

    # ---------------- STUDY OVERVIEW ----------------

    st.subheader("📚 Study Overview")

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "Tasks completed today",
            today_stats["tasks"]
        )

    with b:
        st.metric(
            "Focus sessions today",
            today_stats["focus_sessions"]
        )

    with c:
        st.metric(
            "Study time today",
            f"{today_stats['study_minutes']} min"
        )

    with d:
        st.metric(
            "All-time tasks completed",
            total_tasks_completed
        )

    # ---------------- XP ACTIVITY AND STREAK RECORD ----------------

    a, b = st.columns(2, gap="large")

    with a:

        with st.container(border=True):
            st.subheader("⚡ XP Activity")

            xp_sources = data["xp_sources"]

            st.metric(
                "From task priorities",
                xp_sources["Task XP"]
            )

            st.metric(
                "From daily bonuses",
                xp_sources["Daily bonuses"]
            )

            st.metric(
                "From focus sessions",
                xp_sources["Focus sessions"]
            )

            st.caption(
                "Task XP: Low +5 · Moderate +10 · High +20"
            )

            st.caption(
                "Bonuses: all tasks +20 · "
                "5 tasks in a day +15 · focus session +10"
            )

    with b:

        with st.container(border=True):
            st.subheader("🏆 Streak Record")

            st.metric(
                "Best streak",
                f"{best_streak} days"
            )

            st.write("A productive day means either:")

            st.write(
                "- At least 3 tasks completed, or"
            )

            st.write(
                "- At least 1 completed Focus Timer session"
            )

    # ---------------- ACHIEVEMENTS ----------------

    with st.container(border=True):

        st.subheader("🎖️ Achievements & Badges")

        badge_columns = st.columns(4)

        for index, (
                badge_name,
                earned,
                requirement
        ) in enumerate(get_badges()):

            with badge_columns[index % 4]:

                if earned:

                    st.success(badge_name)
                    st.caption("Unlocked!")

                else:

                    st.info(f"🔒 {badge_name}")
                    st.caption(requirement)


