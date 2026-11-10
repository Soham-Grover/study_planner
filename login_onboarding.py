from email.policy import default

import streamlit as st


def login_onboarding():

    if "user" not in st.session_state:
        st.session_state.user = {"logged_in": False,
                                 "onboarding": False,
                                 "username": "User1",
                                 "email": "email@comapny.com",
                                 "grade": 5,
                                 "board": "cbse",
                                 "subjects": [],
                                 "productive_time": "Morning"
                                 }


    if not st.session_state.user["logged_in"]:
        st.title("Welcome!!")
        st.info(
            "Please Login with you credentials and answer the following questions for that we can personalize your study experience")
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("Username", "Name")
            email = st.text_input("Email", type="email", value="email@gmail.com")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Submit")

            if submitted:
                st.session_state.user["logged_in"] = True
                st.session_state.user["username"] = username
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
            st.session_state.user["onboarding"] = True
            st.session_state.user["grade"] = grade
            st.session_state.user["board"] = board
            st.session_state.user["subjects"] = subjects
            st.session_state.user["productive_time"] = most_productive_time
            st.rerun()

    else:
        st.success("Wohoooo!! You have successfully logged in!!!")
        st.info("Please Use the navigation bar to navigate to you personalized dashboards")

