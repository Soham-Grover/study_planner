from email.policy import default

import streamlit as st

if "user" not in st.session_state or not st.session_state.user.get("logged_in"):
    st.warning("Please log in on the Home page first.")
    st.stop()


st.title("My Profile")
st.header(f" 👤 {st.session_state.user['username']}", divider=True)

st.header("ℹ️ Info")
st.space()

new_email = st.text_input("Change Email", value=f"{st.session_state.user["email"]}", type="email")
st.space("small")
new_grade = st.slider("Change Grade", 5, 12, value=st.session_state.user["grade"])
st.space("small")
new_board = st.selectbox(
            "Change School Board",
            ["CBSE", "ICSE", "IB", "Maharashtra State Board", "Other State Board"],
        )

if new_board == "Other State Board":
    board = st.text_input("Enter Board Name")

st.space("small")

if "editing_subjects" not in st.session_state:
    st.session_state.editing_subjects = False

with st.container(border=True):
    st.subheader("Your Subjects")
    current_subjects = st.session_state.user.get("subjects", [])

    for subject in current_subjects:
        st.text(f"🔖 {subject}")

    if not st.session_state.editing_subjects:
        if st.button("Change Subjects"):
            st.session_state.editing_subjects = True
            st.rerun()
        updated_subjects = current_subjects
    else:
        base_options = (
            [
                "Physics", "Chemistry", "Math", "Biology", "Psychology",
                "Accounts", "Business Studies", "Legal Studies",
                "Computer Science", "Applied Math", "Commercial Arts",
                "Economics", "History", "Geography", "Entrepreneurship",
                "English", "French", "Sanskrit",
            ]
            if new_grade >= 11
            else ["Science", "Math", "SST", "English", "AI", "FMM", "ICT", "Hindi", "Sanskrit", "French"]
        )

        all_options = list(dict.fromkeys(base_options + current_subjects))

        updated_subjects = st.multiselect(
            "Select or type subjects",
            options=all_options,
            default=current_subjects,
            accept_new_options=True,
        )

st.space("small")

st.error("Critical Changes")
new_password = st.text_input("Change Password", type="password")

save_changes = st.button("Save Changes")
