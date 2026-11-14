import streamlit as st
import time
import math
from database import get_quests, update_quest, delete_quest
from database import add_quest, user_auth


if "user" not in st.session_state or not st.session_state.user.get("logged_in"):
    st.warning("Please log in on the Home page first.")
    st.stop()

user_id = st.session_state.user["user_id"]


st.set_page_config(
    layout="wide",
)

# Initialize session state
if "task_ids" not in st.session_state:
    st.session_state.task_ids = []

    db_tasks = get_quests(user_id)


    for quest in db_tasks:
        tid, name, priority, due, is_done = quest
        st.session_state.task_ids.append(tid)
        st.session_state[f"name_{tid}"] = name
        st.session_state[f"priority_{tid}"] = priority
        st.session_state[f"due_{tid}"] = due
        st.session_state[f"done_{tid}"] = bool(is_done)

    st.session_state.tasks_loaded = True
    st.session_state.new_task = ""

# Function to add a task
def add_task():
    task = st.session_state.new_task.strip()

    if task:
        new_tid = add_quest(
            user_id,
            task,
            "Moderate",
            "",
            0
        )

        st.session_state.task_ids.append(new_tid)

        st.session_state[f"name_{new_tid}"] = task
        st.session_state[f"priority_{new_tid}"] = "Moderate"
        st.session_state[f"due_{new_tid}"] = ""
        st.session_state[f"done_{new_tid}"] = False

        st.session_state.new_task = ""


# Function to delete a task
def delete_task(tid):
    delete_quest(tid)
    st.session_state.task_ids.remove(tid)


def sync_task(tid):
    name = st.session_state[f"name_{tid}"]
    priority = st.session_state[f"priority_{tid}"]
    due = st.session_state[f"due_{tid}"]
    done = 1 if st.session_state[f"done_{tid}"] else 0

    update_quest(tid, name, priority, due, done)  # Save to DB
#----------------------*----------------------------

# Master Tabs
t1, t2 = st.tabs(["Daily Planner", "Exam Portal"])

with t1:

    left, right = st.columns([7,3], gap="large")

    # To Do List
    with left:
        with st.container(border=True,key="to_do"):

            # App title
            st.subheader("Daily To-Do List")
            st.markdown("Have all your daily quests managed")


            # Add task section
            col1, col2 = st.columns([4, 1])

            with col1:
                st.text_input(
                    "Add new quest",
                    placeholder="what's awaiting you?",
                    key="new_task"
                )

            with col2:
                st.write("")
                st.button("➕ Add Quest", on_click=add_task)


            # Table headings
            st.divider()

            col1, col2, col3, col4, col5 = st.columns(
                [3, 2, 1, 1, 1]
            )

            col1.write("**Task**")
            col2.write("**Priority**")
            col3.write("**Due**")
            col4.write("**Done**")
            col5.write("**Delete**")


            # Display every task as a separate row
            for i in st.session_state.task_ids:

                col1, col2, col3, col4, col5 = st.columns(
                    [3, 2, 1, 1, 1]
                )

                with col1:
                    st.text_input(
                        "Task",
                        key=f"name_{i}",
                        label_visibility="collapsed",
                        on_change=sync_task, args=(i,)
                    )

                with col2:
                    st.select_slider(
                        "Priority",
                        options=["Low", "Moderate", "High"],
                        key=f"priority_{i}",
                        label_visibility="collapsed",
                        on_change = sync_task, args = (i,)
                    )

                with col3:
                    st.text_input(
                        "Due",
                        key=f"due_{i}",
                        placeholder="Due date",
                        label_visibility="collapsed",
                        on_change=sync_task, args=(i,)

                    )

                with col4:
                    st.checkbox(
                        "Done",
                        key=f"done_{i}",
                        label_visibility="collapsed",
                        on_change=sync_task, args=(i,)
                    )

                with col5:
                    st.button(
                        "🗑️",
                        key=f"delete_{i}",
                        on_click=delete_task,
                        args=(i,)
                    )

    # Progress Tracker
    with right:
        with st.container(border=True):

            st.subheader("Progress Tracker")

            total = len(st.session_state.task_ids)

            completed = sum(
                st.session_state[f"done_{i}"]
                for i in st.session_state.task_ids
            )

            percentage = int((completed / total) * 100) if total > 0 else 0

            # Different gradient for 100% completion
            if percentage == 100:
                ring_gradient = """
                    conic-gradient(
                        from -90deg,
                        #bbf7d0 0%,
                        #86efac 25%,
                        #4ade80 50%,
                        #15803d 75%,
                        #bbf7d0 100%
                    )
                """
            else:
                p1 = percentage * 0.35
                p2 = percentage * 0.70

                ring_gradient = f"""
                    conic-gradient(
                        from -90deg,
                        #bbf7d0 0%,
                        #86efac {p1}%,
                        #4ade80 {p2}%,
                        #15803d {percentage}%,
                        #e5e7eb {percentage}% 100%
                    )
                """

            st.html(
                f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    margin: 20px auto;
                ">
                    <div style="
                        width: 150px;
                        height: 150px;
                        position: relative;
                    ">

                        <div style="
                            width: 150px;
                            height: 150px;
                            border-radius: 50%;
                            background: {ring_gradient};

                            -webkit-mask: radial-gradient(
                                farthest-side,
                                transparent 80%,
                                black 81%
                            );

                            mask: radial-gradient(
                                farthest-side,
                                transparent 80%,
                                black 81%
                            );
                        "></div>

                        <div style="
                            position: absolute;
                            inset: 0;
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            color: white;
                        ">
                            <span style="
                                font-size: 28px;
                                font-weight: bold;
                            ">{percentage}%</span>

                            <span style="
                                font-size: 12px;
                                opacity: 0.7;
                            ">Completed</span>
                        </div>

                    </div>
                </div>
                """
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"<h2>{total}</h2>", unsafe_allow_html=True)
                st.caption("Total")

            with col2:
                st.markdown(f"<h2>{completed}</h2>", unsafe_allow_html=True)
                st.caption("Done")

            with col3:
                st.markdown(f"<h2>{total - completed}</h2>", unsafe_allow_html=True)
                st.caption("Pending")

            # Celebrate only when progress reaches 100%
            if percentage == 100:
                st.balloons()


    left, right = st.columns([7, 3], gap="large")


    # Focus Timer Functions
    def start_timer():

        minutes = st.session_state.study_minutes

        st.session_state.study_remaining = minutes * 60

        st.session_state.phase = "Study"

        st.session_state.phase_seconds = min(
            minutes * 60, 45 * 60
        )

        st.session_state.timer_remaining = (
            st.session_state.phase_seconds
        )

        st.session_state.timer_end = (
            time.time() + st.session_state.phase_seconds
        )

        st.session_state.timer_running = True


    def pause_timer():

        remaining = max(
            0,
            math.ceil(st.session_state.timer_end - time.time())
        )

        st.session_state.timer_remaining = remaining
        st.session_state.timer_running = False


    def resume_timer():

        st.session_state.timer_end = (
            time.time() + st.session_state.timer_remaining
        )

        st.session_state.timer_running = True


    def reset_timer():

        st.session_state.timer_running = False
        st.session_state.study_remaining = 0
        st.session_state.timer_remaining = 0
        st.session_state.phase = "Not Started"
        st.session_state.phase_seconds = 0
        st.session_state.timer_end = 0


    # Initialize timer session state

    if "timer_running" not in st.session_state:

        st.session_state.timer_running = False
        st.session_state.study_remaining = 0
        st.session_state.timer_remaining = 0
        st.session_state.phase = "Not Started"
        st.session_state.phase_seconds = 0
        st.session_state.timer_end = 0

    # Focus Timer
    with right:
        with st.container(border=True):

            st.subheader("Focus Timer")

            @st.fragment(run_every="1s")
            def focus_timer():

                # Study duration input

                st.number_input(
                    "Study time (minutes)",
                    min_value=15,
                    max_value=240,
                    value=60,
                    step=5,
                    key="study_minutes",
                    disabled=st.session_state.phase != "Not Started"
                )

                # Timer calculation

                if st.session_state.timer_running:

                    remaining = max(
                        0,
                        math.ceil(
                            st.session_state.timer_end - time.time()
                        )
                    )

                    # When a study/break session finishes

                    if remaining == 0:

                        if st.session_state.phase == "Study":

                            st.session_state.study_remaining -= (
                                st.session_state.phase_seconds
                            )

                            if st.session_state.study_remaining > 0:

                                # Start 10-minute break

                                st.session_state.phase = "Break"
                                st.session_state.phase_seconds = 10 * 60

                                st.session_state.timer_end = (
                                    time.time() + 10 * 60
                                )

                            else:

                                # All study time completed

                                st.session_state.phase = "Completed"
                                st.session_state.timer_running = False

                        elif st.session_state.phase == "Break":

                            # Start next study session

                            st.session_state.phase = "Study"

                            st.session_state.phase_seconds = min(
                                st.session_state.study_remaining,
                                45 * 60
                            )

                            st.session_state.timer_end = (
                                time.time()
                                + st.session_state.phase_seconds
                            )

                    else:

                        st.session_state.timer_remaining = remaining

                else:

                    remaining = st.session_state.timer_remaining

                # ---------------- CIRCULAR TIMER ----------------

                if st.session_state.phase == "Not Started":

                    percentage = 0
                    display_time = "00:00"
                    label = "Ready to Focus"

                elif st.session_state.phase == "Completed":

                    percentage = 100
                    display_time = "00:00"
                    label = "Completed"

                else:

                    percentage = (
                        1 - remaining / st.session_state.phase_seconds
                    ) * 100

                    minutes = remaining // 60
                    seconds = remaining % 60

                    display_time = f"{minutes:02d}:{seconds:02d}"

                    if st.session_state.phase == "Study":
                        label = "Focus Time"
                    else:
                        label = "Break Time"

                # Blue circular ring

                st.html(f"""
                    <div style="
                        display:flex;
                        justify-content:center;
                        align-items:center;
                        position:relative;
                        height:190px;
                        margin:15px 0;
                    ">

                        <div style="
                            width:170px;
                            height:170px;
                            border-radius:50%;

                            background:conic-gradient(
                                from -90deg,
                                #bfdbfe 0%,
                                #60a5fa {percentage * 0.5}%,
                                #2563eb {percentage}%,
                                #e5e7eb {percentage}% 100%
                            );

                            -webkit-mask:radial-gradient(
                                farthest-side,
                                transparent 84%,
                                black 85%
                            );

                            mask:radial-gradient(
                                farthest-side,
                                transparent 84%,
                                black 85%
                            );
                        "></div>

                        <div style="
                            position:absolute;
                            display:flex;
                            flex-direction:column;
                            align-items:center;
                            justify-content:center;
                            pointer-events:none;
                        ">

                            <span style="
                                font-size:30px;
                                font-weight:bold;
                                color:#2563eb;
                            ">{display_time}</span>

                            <span style="
                                font-size:13px;
                                color:#64748b;
                            ">{label}</span>

                        </div>

                    </div>
                """)

                # ---------------- TIMER BUTTONS ----------------

                col1, col2, col3 = st.columns(3)

                with col1:

                    if st.session_state.phase in [
                        "Not Started", "Completed"
                    ]:

                        st.button(
                            "▶ Start",
                            on_click=start_timer,
                            use_container_width=True
                        )

                with col2:

                    if st.session_state.timer_running:

                        st.button(
                            "⏸ Pause",
                            on_click=pause_timer,
                            use_container_width=True
                        )

                    elif st.session_state.phase not in [
                        "Not Started", "Completed"
                    ]:

                        st.button(
                            "▶ Resume",
                            on_click=resume_timer,
                            use_container_width=True
                        )

                with col3:

                    st.button(
                        "↻ Reset",
                        on_click=reset_timer,
                        use_container_width=True
                    )

            focus_timer()