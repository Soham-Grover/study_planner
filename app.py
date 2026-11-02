import streamlit as st

if "login" not in st.session_state:
    st.session_state["login"] = 0

st.header("Welcome to Study Planner - Let's Personalize your experience first!!!")

if st.session_state["login"] == 0:

    st.subheader("Login")

    username = st.text_input("Username")
    password = 