import streamlit as st
import time
import math
import json
from pathlib import Path
from datetime import date
from database import get_quests, update_quest, delete_quest, add_quest

if "user" not in st.session_state or not st.session_state.user.get("logged_in"):
    st.warning("Please log in on the Home page first.")
    st.stop()

user_id = st.session_state.user["user_id"]


db_tasks = get_quests(user_id)
st.session_state.task_ids = []
for quest in db_tasks:
    tid, name, priority, due, is_done = quest
    st.session_state.task_ids.append(tid)
    st.session_state[f"name_{tid}"] = name
    st.session_state[f"priority_{tid}"] = priority if priority in ["Low", "Moderate", "High"] else "Moderate"
    st.session_state[f"due_{tid}"] = due or ""
    st.session_state[f"done_{tid}"] = bool(is_done)


def add_task():
    task = st.session_state.get("new_task", "").strip()
    if task:
        new_tid = add_quest(user_id, task, "Moderate", "", 0)
        st.session_state.task_ids.append(new_tid)
        st.session_state[f"name_{new_tid}"] = task
        st.session_state[f"priority_{new_tid}"] = "Moderate"
        st.session_state[f"due_{new_tid}"] = ""
        st.session_state[f"done_{new_tid}"] = False
        st.session_state.new_task = ""


def delete_task(tid):
    delete_quest(tid)
    if tid in st.session_state.task_ids:
        st.session_state.task_ids.remove(tid)
    for prefix in ["name_", "priority_", "due_", "done_"]:
        st.session_state.pop(f"{prefix}{tid}", None)


def sync_task(tid):
    name = st.session_state.get(f"name_{tid}")
    is_done = st.session_state.get(f"done_{tid}", False)
    priority = st.session_state.get(f"priority_{tid}")
    due = st.session_state.get(f"due_{tid}")
    update_quest(tid, name, priority, due, 1 if is_done else 0)

    if is_done:
        award_task_xp(tid)


def start_timer():
    minutes = st.session_state.study_minutes
    st.session_state.study_remaining = minutes * 60
    st.session_state.phase = "Study"
    st.session_state.phase_seconds = min(minutes * 60, 45 * 60)
    st.session_state.timer_remaining = st.session_state.phase_seconds
    st.session_state.timer_end = time.time() + st.session_state.phase_seconds
    st.session_state.timer_running = True


def pause_timer():
    st.session_state.timer_remaining = max(0, math.ceil(st.session_state.timer_end - time.time()))
    st.session_state.timer_running = False


def resume_timer():
    st.session_state.timer_end = time.time() + st.session_state.timer_remaining
    st.session_state.timer_running = True


def reset_timer():
    st.session_state.timer_running = False
    st.session_state.study_remaining = 0
    st.session_state.timer_remaining = 0
    st.session_state.phase = "Not Started"
    st.session_state.phase_seconds = 0
    st.session_state.timer_end = 0


if "timer_running" not in st.session_state:
    reset_timer()


left, right = st.columns([7, 3], gap="large")

with left:
    with st.container(border=True, key="to_do"):
        st.subheader("Daily To-Do List")
        st.markdown("Have all your daily quests managed")

        col1, col2 = st.columns([4, 1])
        with col1:
            st.text_input("Add new quest", placeholder="What's awaiting you?", key="new_task")
        with col2:
            st.write("")
            st.button("➕ Add Quest", on_click=add_task)

        st.divider()
        col1, col2, col3, col4, col5 = st.columns([3, 2, 1.5, 0.8, 0.8])
        col1.write("**Task**")
        col2.write("**Priority**")
        col3.write("**Due**")
        col4.write("**Done**")
        col5.write("**Delete**")

        for i in st.session_state.task_ids:
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1.5, 0.8, 0.8])
            with col1:
                st.text_input("Task", key=f"name_{i}", label_visibility="collapsed", on_change=sync_task, args=(i,))
            with col2:
                st.select_slider(
                    "Priority",
                    options=["Low", "Moderate", "High"],
                    key=f"priority_{i}",
                    label_visibility="collapsed",
                    on_change=sync_task,
                    args=(i,),
                )
            with col3:
                st.text_input(
                    "Due",
                    key=f"due_{i}",
                    placeholder="Due date",
                    label_visibility="collapsed",
                    on_change=sync_task,
                    args=(i,),
                )
            with col4:
                st.checkbox("Done", key=f"done_{i}", label_visibility="collapsed", on_change=sync_task, args=(i,))
            with col5:
                st.button("🗑️", key=f"delete_{i}", on_click=delete_task, args=(i,))

        if st.session_state.task_ids and all(
            st.session_state.get(f"done_{tid}", False) for tid in st.session_state.task_ids
        ):
            award_all_tasks_bonus()

with right:
    with st.container(border=True):
        st.subheader("Progress Tracker")
        total = len(st.session_state.task_ids)
        completed = sum(1 for i in st.session_state.task_ids if st.session_state.get(f"done_{i}", False))
        percentage = int((completed / total) * 100) if total > 0 else 0

        if percentage == 100:
            ring_gradient = "conic-gradient(from -90deg, #bbf7d0 0%, #86efac 25%, #4ade80 50%, #15803d 75%, #bbf7d0 100%)"
        else:
            p1, p2 = percentage * 0.35, percentage * 0.70
            ring_gradient = f"conic-gradient(from -90deg, #bbf7d0 0%, #86efac {p1}%, #4ade80 {p2}%, #15803d {percentage}%, #e5e7eb {percentage}% 100%)"

        st.html(
            f"""
            <div style="display:flex; justify-content:center; margin:20px auto;">
                <div style="width:150px; height:150px; position:relative;">
                    <div style="width:150px; height:150px; border-radius:50%; background:{ring_gradient};
                        -webkit-mask:radial-gradient(farthest-side, transparent 80%, black 81%);
                        mask:radial-gradient(farthest-side, transparent 80%, black 81%);"></div>
                    <div style="position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                        <span style="font-size:28px; font-weight:bold;">{percentage}%</span>
                        <span style="font-size:12px; opacity:0.7;">Completed</span>
                    </div>
                </div>
            </div>
            """
        )

        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<h2>{total}</h2>", unsafe_allow_html=True)
        c1.caption("Total")
        c2.markdown(f"<h2>{completed}</h2>", unsafe_allow_html=True)
        c2.caption("Done")
        c3.markdown(f"<h2>{total - completed}</h2>", unsafe_allow_html=True)
        c3.caption("Pending")

        if percentage == 100 and total > 0:
            st.balloons()

    # ---------------- FOCUS TIMER ----------------
    #_, right_timer = st.columns([7, 3], gap="large")
    #with right_timer:
    with st.container(border=True):
        st.subheader("Focus Timer")

        @st.fragment(run_every="1s")
        def focus_timer():
            st.number_input(
                "Study time (minutes)",
                min_value=15,
                max_value=240,
                value=60,
                step=5,
                key="study_minutes",
                disabled=st.session_state.phase != "Not Started",
            )

            if st.session_state.timer_running:
                remaining = max(0, math.ceil(st.session_state.timer_end - time.time()))
                if remaining == 0:
                    if st.session_state.phase == "Study":
                        st.session_state.study_remaining -= st.session_state.phase_seconds
                        if st.session_state.study_remaining > 0:
                            st.session_state.phase = "Break"
                            st.session_state.phase_seconds = 10 * 60
                            st.session_state.timer_end = time.time() + 10 * 60
                        else:
                            record_focus_session()
                            st.session_state.phase = "Completed"
                            st.session_state.timer_running = False
                    elif st.session_state.phase == "Break":
                        st.session_state.phase = "Study"
                        st.session_state.phase_seconds = min(st.session_state.study_remaining, 45 * 60)
                        st.session_state.timer_end = time.time() + st.session_state.phase_seconds
                else:
                    st.session_state.timer_remaining = remaining
            else:
                remaining = st.session_state.timer_remaining

            if st.session_state.phase == "Not Started":
                percentage, display_time, label = 0, "00:00", "Ready to Focus"
            elif st.session_state.phase == "Completed":
                percentage, display_time, label = 100, "00:00", "Completed"
            else:
                percentage = (1 - remaining / st.session_state.phase_seconds) * 100
                minutes, seconds = divmod(remaining, 60)
                display_time = f"{minutes:02d}:{seconds:02d}"
                label = "Focus Time" if st.session_state.phase == "Study" else "Break Time"

            st.html(
                f"""
                <div style="display:flex; justify-content:center; align-items:center; position:relative; height:190px; margin:15px 0;">
                    <div style="width:170px; height:170px; border-radius:50%;
                        background:conic-gradient(from -90deg, #bfdbfe 0%, #60a5fa {percentage * 0.5}%, #2563eb {percentage}%, #e5e7eb {percentage}% 100%);
                        -webkit-mask:radial-gradient(farthest-side, transparent 84%, black 85%);
                        mask:radial-gradient(farthest-side, transparent 84%, black 85%);"></div>
                    <div style="position:absolute; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                        <span style="font-size:30px; font-weight:bold; color:#2563eb;">{display_time}</span>
                        <span style="font-size:13px; color:#64748b;">{label}</span>
                    </div>
                </div>
                """
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.session_state.phase in ["Not Started", "Completed"]:
                    st.button("▶ Start", on_click=start_timer, use_container_width=True)
            with col2:
                if st.session_state.timer_running:
                    st.button("⏸ Pause", on_click=pause_timer, use_container_width=True)
                elif st.session_state.phase not in ["Not Started", "Completed"]:
                    st.button("▶ Resume", on_click=resume_timer, use_container_width=True)
            with col3:
                st.button("↻ Reset", on_click=reset_timer, use_container_width=True)

        focus_timer()