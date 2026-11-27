from login_onboarding import login_onboarding
import streamlit as st
from login_onboarding import logout

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.logo(
    "stride-nobg.png",
    size="large"
)

# Custom CSS for logo size
st.markdown("""
<style>
[data-testid="stSidebarHeader"] img {
    width: 80px !important;
    height: auto !important;
    object-fit: contain;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Stride", layout="wide", initial_sidebar_state="collapsed")

def load_css(file_name="styles.css"):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

pages = [
    st.Page(login_onboarding, title="Home", icon="🏠", default=True),
    st.Page("pages/daily_dashboard.py", title="Dashboard", icon="📊"),
    st.Page("pages/daily_planner.py", title="Daily Planner", icon="📝"),
    st.Page("pages/exam_portal.py", title="AI Exam Portal", icon="🎓"),
    st.Page("pages/profile.py", title="My Profile", icon="👤"),
    st.Page("pages/about.py", title="About Stride", icon="ℹ️")
]

pg = st.navigation(pages)
pg.run()

if st.session_state.user["logged_in"]:
    with st.sidebar:
        st.write(f"👤 **{st.session_state.user['username']}**")
        st.button("Logout", on_click=logout, use_container_width=True)

