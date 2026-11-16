from email.policy import default
import streamlit as st
import database
from database import add_user, user_auth, add_student_profile, get_student_profile


def login_onboarding():

    if "user" not in st.session_state:
        st.session_state.user = {"logged_in": False,
                                 "onboarding": False,
                                 "user_id": 123,
                                 "username": "User1",
                                 "email": "email@comapny.com",
                                 "grade": 5,
                                 "board": "cbse",
                                 "subjects": [],
                                 "productive_time": "Morning",
                                 "study_hours": 2
                                 }

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:

        if not st.session_state.user["logged_in"]:
            st.title("Welcome Back!!")
            st.info(
                "Please Login with you credentials and answer the following questions for that we can personalize your study experience")
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input("Username", "Name")
                password = st.text_input("Password", type="password")

                submitted = st.form_submit_button("Submit")

                if submitted:
                    logged_in_userid = user_auth(username, password)
                    profile = get_student_profile(logged_in_userid)
                    if logged_in_userid:
                        st.session_state.user["logged_in"] = True
                        st.session_state.user["username"] = username
                        st.session_state.user["user_id"] = logged_in_userid

                        if profile:
                            st.session_state.user["grade"] = profile["grade"]
                            st.session_state.user["board"] = profile["board"]
                            st.session_state.user["subjects"] = profile["subjects"]
                            st.session_state.user["productive_time"] = profile["productive_time"]
                            st.session_state.user["study_hours"] = profile["study_hours"]
                            st.session_state.user["onboarding"] = True
                            st.balloons()
                        else:
                            st.session_state.user["onboarding"] = False

                        st.rerun()
                    else:
                        st.warning("Wrong username or password")

    with signup_tab:

        if not st.session_state.user["logged_in"]:
            st.title("Welcome!!")
            st.info(
                "Enter your credentials to jump back into studying")
            with st.form("signup_form", clear_on_submit=True):
                username = st.text_input("Username", "Name")
                email = st.text_input("Email", type="email", value="email@gmail.com")
                password = st.text_input("Password", type="password")

                submitted = st.form_submit_button("Submit")

                if submitted:
                    new_userid = add_user(username, email, password)
                    st.balloons()
                    if new_userid:
                        st.session_state.user["logged_in"] = True
                        st.session_state.user["username"] = username
                        st.session_state.user["user_id"] = new_userid
                        st.rerun()

        elif st.session_state.user["logged_in"] and not st.session_state.user["onboarding"]:

            st.title("Lets Personalize Your Experience")

            grade = st.slider("Enter Your Grade", 5, 12)
            board = st.selectbox("Select Your School Board", ["CBSE", "ICSE", "IB", "Maharashtra State Board", "Other State Board"])

            if board == "Other State Board":
                board = st.text_input("Enter Board Name")

            if grade >= 11:
                subjects = st.multiselect("Subjects", ["Physics", "Chemistry", "Math", "Biology", "Psychology", "Accounts", "Business Studies",
                                                       "Legal Studies", "Computer Science", "Applied Math", "Commercial Arts", "Economics", "History", "Geography", "Entrepreneurship", "English", "French", "Sanskrit"])

            else:
                subjects = st.multiselect("Subjects", ["Science", "Math", "SST", "English", "AI", "FMM", "ICT", "Hindi", "Sanskrit", "French"])

            study_hours = st.slider("How many hours do you devote to studying after school", 0, 12)

            most_productive_time = st.multiselect("When are you the most productive?", ["Morning before school", "Afternoon just after school", "Late Evening"])

            submit_button_questions = st.button("Personalize My Experience")

            if submit_button_questions:
                add_student_profile(st.session_state.user["user_id"], grade, board, subjects, most_productive_time, study_hours)
                st.session_state.user["onboarding"] = True
                st.session_state.user["grade"] = grade
                st.session_state.user["board"] = board
                st.session_state.user["subjects"] = subjects
                st.session_state.user["productive_time"] = most_productive_time
                st.session_state.user["study_hours"] = study_hours
                st.rerun()

        else:
            st.success("Wohoooo!! You have successfully logged in!!!")
            st.info("Please Use the navigation bar to navigate to you personalized dashboards")

