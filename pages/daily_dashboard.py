import streamlit as st

if st.session_state["login"] == 1:
    st.text("Logged In")

else:
    st.text("Not Logged In yet, login on the main screen first")