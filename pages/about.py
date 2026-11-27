import streamlit as st

st.set_page_config(layout="wide")

if "user" not in st.session_state or not st.session_state.user.get("logged_in"):
    st.warning("Login on the Home page first.")
    st.stop()

#-------------WELCOME----------------
with st.container(border=True):
    st.subheader("WELCOME TO STRIDE!")
    st.markdown(
        "<h4 style='margin-top: -10px; color: #8B9CFF;'>"
        "Less CHAOS. More CLOCKED-IN."
        "</h4>",
        unsafe_allow_html=True
    )
    st.write("Your all-in-one space to organise your studies, stay focused, track your progress and turn your goals into achievements.")
    st.divider()
    a1, a2, a3 = st.columns(3)
    with a1:
        st.write("PLAN SMARTER")
    with a2:
        st.write("FOCUS BETTER")
    with a3:
        st.write("ACHIEVE MORE")

st.write("")
st.write("")
st.write("")

#-----------WHAT AND WHY STRIDE---------------
b1, b2 = st.columns(2)
with b1:
    with st.container(border=True, height=230):
        st.markdown(
                "<h4 style='margin-top: -10px; color: #8B9CFF;'>"
                "What is STRIDE?"
                "</h4>",
                unsafe_allow_html=True
            )
        st.write("STRIDE is an all-in-one student productivity platform designed to make academic life more organised, focused and rewarding. It brings together essential study tools, from managing daily tasks and tracking productivity to creating personalised exam timetables and keeping track of chapters. With STRIDE, you can plan your day, manage your exam preparation, stay focused and monitor your progress — all in one place.")
with b2:
    with st.container(border=True, height=230):
        st.markdown(
                "<h4 style='margin-top: -10px; color: #8B9CFF;'>"
                "Why STRIDE?"
                "</h4>",
                unsafe_allow_html=True
            )
        st.write("Managing academics involves more than just studying. Balancing assignments, deadlines, exam preparation and daily goals can sometimes become overwhelming. STRIDE aims to simplify this journey by bringing everything together in one platform. It helps you: Stay organised and manage your time effectively. Build consistent study and focus habits. Plan exam preparation with personalised timetables. Keep track of chapters and academic progress. Stay motivated through XP, levels and achievements. Because productivity isn't about doing everything at once — it's about making consistent progress, one step at a time.")


st.write("")
st.write("")
st.write("")


#---------------FEATURES-----------------

st.markdown("""
    <style>
    .feature-card {
        border: 1px solid rgba(128,128,128,0.3);
        border-radius: 14px;
        padding: 20px;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        border-color: #8B9CFF;
        box-shadow: 0 5px 18px rgba(100,100,255,0.15);
        background-color: rgba(139,156,255,0.06);
    }

    .feature-title {
        font-size: 19px;
        font-weight: 600;
    }

    .feature-content {
        opacity: 0;
        transition: opacity 0.3s ease;
        margin-top: 15px;
        visibility:none;
    }

    .feature-card:hover .feature-content {
        opacity: 1;
        visibility:true;
    }

    .feature-content img {
        width: 100%;
        border-radius: 10px;
        margin-top: 10px;
    }
    </style>""", unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📝Daily Planner • To-do list</div>

            <div class="feature-content">
                <p>
                Organise your day by managing tasks, setting priorities
                and keeping track of deadlines.
                </p>

                <ul>
                    <li>Add, manage and categorise daily tasks.</li>
                    <li>Set task priorities and due date.</li>
                    <li>Track completed tasks.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📊 Progress Tracker • Focus Sessions</div>
        
            <div class="feature-content">
                <p>
                    Monitor your productivity, build consistency and
                    understand how you're progressing towards your goals.
                </p>
        
                <ul>
                    <li>Track your total XP and current level.</li>
                    <li>Monitor your daily productivity streak.</li>
                    <li>Keep track of your focus sessions.</li>
                    <li>Earn badges and celebrate achievements.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

st.write("")

c3, c4 = st.columns(2)

with c3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎓 Exam Portal • Personalised Timetable</div>

            <div class="feature-content">
                <p>
                    Make exam preparation easier with a study timetable
                    tailored to your academic schedule and preparation needs.
                </p>

                <ul>
                    <li>Create personalised study timetables.</li>
                    <li>Organise your exam preparation.</li>
                    <li>Allocate study time to your subjects.</li>
                    <li>Plan your preparation in a structured way.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c4:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📚 Chapter List • Subject-wise Organisation</div>

            <div class="feature-content">
                <p>
                    Keep your syllabus organised with subject-wise
                    chapter lists and make it easier to track your preparation.
                </p>

                <ul>
                    <li>View chapters organised by subject.</li>
                    <li>Keep track of your syllabus.</li>
                    <li>Identify chapters that need attention.</li>
                    <li>Make your exam preparation more organised.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True
    )


st.write("")
st.write("")
st.write("")


#--------------------FIRST STEP----------------
st.subheader("🚀 READY TO MAKE YOUR FIRST STRIDE?")
st.caption("Your journey towards smarter studying starts here.")

st.write("")

# Step 1 and Step 2
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown(
                "<h4 style='margin-top: -10px; color: #8B9CFF;'>"
                "📝 01 — Plan Your Day"
                "</h4>",
                unsafe_allow_html=True
            )
        st.write(
            "Add tasks, set priorities and organise "
            "your daily goals using the Daily Planner."
        )

with col2:
    with st.container(border=True):
        st.markdown(
                "<h4 style='margin-top: -10px; color: #8B9CFF;'>"
                "⏱️ 02 — Stay Focused"
                "</h4>",
                unsafe_allow_html=True
            )
        st.write(
            "Use focus sessions to build productive "
            "study habits and make the most of your time."
        )

# Step 3 and Step 4
col3, col4 = st.columns(2, gap="large")

with col3:
    with st.container(border=True):
        st.markdown(
                "<h4 style='margin-top: -10px; color: #8B9CFF;'>"
                "🎓 03 — Prepare for Exams"
                "</h4>",
                unsafe_allow_html=True
            )
        st.write(
            "Create a personalised study timetable "
            "and keep track of your subject-wise chapters."
        )

with col4:
    with st.container(border=True):
        st.markdown(
                "<h4 style='margin-top: -10px; color: #8B9CFF;'>"
                "🏆 04 — Track Your Progress"
                "</h4>",
                unsafe_allow_html=True
            )
        st.write(
            "Earn XP, unlock achievements and monitor "
            "your progress as you reach your goals."
        )

st.write("")
st.write("")
st.write("")


#-----------END----------------
st.markdown("""
<style>
.stride-footer {
    background-color: rgba(139, 92, 246, 0.08);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
}
</style>

<div class="stride-footer">
    <h2>Every big achievement begins with one small step.</h2>
    <p>PLAN SMARTER &nbsp; • &nbsp; FOCUS BETTER &nbsp; • &nbsp; ACHIEVE MORE</p>
</div>
""", unsafe_allow_html=True)