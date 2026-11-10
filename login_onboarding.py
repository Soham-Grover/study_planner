import streamlit as st


def login_onboarding():

    if "user" not in st.session_state:
        st.session_state.user = {"logged_in": False,
                                 "username": "User1",
                                 "email": "email@comapny.com",
                                 "grade": 5,
                                 "board": "cbse",
                                 }


    if not st.session_state.user["logged_in"]:
        st.title("Welcome!!")
        st.subheader(
            "Please Login with you credentials and answer the following questions for that we can personalize your study experience")
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("Username")
            email = st.text_input("Email", type="email")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Submit")

            if submitted:
                st.session_state.user["logged_in"] = True
                st.session_state.user["username"] = username
                st.rerun()


    elif st.session_state.logged_in and not st.session_state.onboarded:

        with st.form:

            grade = st.slider("Enter Your Grade", 5, 12)
            board = st.selectbox("Select Your School Board", ["CBSE", "ICSE", "IB", "Maharashtra State Board", "Other State Board"])

            if board == "Other State Board":
                board = st.text_input("Enter Board Name")

            if grade >= 11:
                subjects = st.multiselect("Subjects", ["Physics", "Chemistry", "Math", "Biology", "P"])
