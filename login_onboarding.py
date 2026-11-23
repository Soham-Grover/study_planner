import sqlite3
import streamlit as st
from database import add_user, user_auth, add_student_profile, get_student_profile


def logout():
    st.session_state.user = {
        "logged_in": False,
        "onboarding": False,
        "user_id": None,
        "username": "",
        "email": "",
        "grade": 5,
        "board": "CBSE",
        "subjects": [],
        "productive_time": [],
        "study_hours": 2,
    }
    st.session_state.pop("plan_loaded_user", None)
    st.session_state.pop("loaded_user_id", None)


def login_onboarding():
    if "user" not in st.session_state:
        st.session_state.user = {
            "logged_in": False,
            "onboarding": False,
            "user_id": None,
            "username": "",
            "email": "",
            "grade": 5,
            "board": "CBSE",
            "subjects": [],
            "productive_time": [],
            "study_hours": 2,
        }

    # CASE 1: Logged in AND onboarding completed -> Redirect to Daily Dashboard
    if st.session_state.user["logged_in"] and st.session_state.user["onboarding"]:
        st.switch_page("pages/daily_dashboard.py")

    # CASE 2: Signed up, logged in, but onboarding NOT completed -> Show Questionnaire
    elif st.session_state.user["logged_in"] and not st.session_state.user["onboarding"]:
        st.title("Let's Personalize Your Experience")
        st.info("Answer a few quick questions so Stride can tailor your study plan.")

        grade = st.slider("Enter Your Grade", 5, 12, value=10)
        board = st.selectbox(
            "Select Your School Board",
            ["CBSE", "ICSE", "IB", "Maharashtra State Board", "Other State Board"],
        )

        if board == "Other State Board":
            board = st.text_input("Enter Board Name")

        if grade >= 11:
            subjects = st.multiselect(
                "Subjects",
                [
                    "Physics", "Chemistry", "Math", "Biology", "Psychology",
                    "Accounts", "Business Studies", "Legal Studies",
                    "Computer Science", "Applied Math", "Commercial Arts",
                    "Economics", "History", "Geography", "Entrepreneurship",
                    "English", "French", "Sanskrit",
                ],
            )
        else:
            subjects = st.multiselect(
                "Subjects",
                ["Science", "Math", "SST", "English", "AI", "FMM", "ICT", "Hindi", "Sanskrit", "French"],
            )

        study_hours = st.slider("How many hours do you devote to studying after school?", 0, 12, value=2)
        most_productive_time = st.multiselect(
            "When are you the most productive?",
            ["Morning before school", "Afternoon just after school", "Late Evening"],
        )

        if st.button("Personalize My Experience", type="primary"):
            add_student_profile(
                st.session_state.user["user_id"],
                grade,
                board,
                subjects,
                most_productive_time,
                study_hours,
            )
            st.session_state.user["onboarding"] = True
            st.session_state.user["grade"] = grade
            st.session_state.user["board"] = board
            st.session_state.user["subjects"] = subjects
            st.session_state.user["productive_time"] = most_productive_time
            st.session_state.user["study_hours"] = study_hours
            st.switch_page("pages/daily_dashboard.py")

    # CASE 3: Not logged in -> Show Login & Sign Up tabs
    else:
        st.markdown(
            """
            <div style="text-align: center; padding: 10px 0 20px 0;">
                <h1 style="margin-bottom: 0; letter-spacing: 2px;">STRIDE</h1>
                <p style="color: #94a3b8; font-size: 16px; margin-top: 4px;">
                    From chaos to clocked-in.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

        with login_tab:
            st.subheader("Welcome Back!")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)

                if submitted:
                    logged_in_userid = user_auth(username.strip(), password)
                    if logged_in_userid:
                        profile = get_student_profile(logged_in_userid)
                        st.session_state.user["logged_in"] = True
                        st.session_state.user["username"] = username.strip()
                        st.session_state.user["user_id"] = logged_in_userid

                        if profile:
                            st.session_state.user["grade"] = profile["grade"]
                            st.session_state.user["board"] = profile["board"]
                            st.session_state.user["subjects"] = profile["subjects"]
                            st.session_state.user["productive_time"] = profile["productive_time"]
                            st.session_state.user["study_hours"] = profile["study_hours"]
                            st.session_state.user["onboarding"] = True
                            st.switch_page("pages/daily_dashboard.py")
                        else:
                            st.session_state.user["onboarding"] = False
                            st.rerun()
                    else:
                        st.error("Wrong username or password.")

        with signup_tab:
            st.subheader("Create an Account")
            with st.form("signup_form"):
                new_username = st.text_input("Username")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign Up", use_container_width=True)

                if submitted:
                    if not new_username.strip() or not new_email.strip() or not new_password:
                        st.warning("Please fill in all fields.")
                    else:
                        try:
                            new_userid = add_user(new_username.strip(), new_email.strip(), new_password)
                            st.session_state.user["logged_in"] = True
                            st.session_state.user["onboarding"] = False
                            st.session_state.user["username"] = new_username.strip()
                            st.session_state.user["email"] = new_email.strip()
                            st.session_state.user["user_id"] = new_userid
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("That username or email is already taken.")