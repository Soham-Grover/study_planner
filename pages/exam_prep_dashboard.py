import streamlit as st
import tempfile
from pypdf import PdfReader
from agents.info_extractor_agent import *
from agents.planner_agent import day_wise_plan_chain
import datetime
from datetime import date

if "user" not in st.session_state or not st.session_state.user["logged_in"] or not st.session_state.user["onboarding"]:
    st.warning("Login on the Home page first.")


else:

    if "day_wise_plan" not in st.session_state:
        st.session_state["day_wise_plan"] = None

    if "plan_generated" not in st.session_state:
        st.session_state["plan_generated"] = False

    if not st.session_state["plan_generated"]:

        st.title(f"Let's crush that exam, {st.session_state.user["username"]}!!")
        st.space()
        # Uploading File
        uploaded_file = st.file_uploader("Upload Syllabus and Date Sheet for Your Upcoming Examination")

        # Extracting Raw Data from File
        if uploaded_file is not None:
            reader = PdfReader(uploaded_file)

            syllabus_datesheet = ""

            for page in reader.pages:
                syllabus_datesheet += page.extract_text() + "\n"

        strengths = st.multiselect("What subjects are your strongest?", st.session_state.user["subjects"])
        views_on_syllabus = st.text_area("What does your overall preparation seem to you?")

        extract_data_button = st.button("Generate Personalized Exam Preparation Plan")

        if extract_data_button:
            info_extracted = info_extractor_chain.invoke(input={"name": st.session_state.user["username"],
                                               "grade": st.session_state.user["grade"],
                                               "subjects": st.session_state.user["subjects"],
                                               "strengths": strengths,
                                                "board": st.session_state.user["board"],
                                               "views_on_syllabus": views_on_syllabus,"syllabus_datesheet_text": syllabus_datesheet})


            subject_list = []
            chapter_list = []

            for item in info_extracted.chapter_list:
                subject_list.append(item.subject_name)
                chapter_list.append(item.chapters)

            

            exam_dates = []
            exam_dates_subject_ordered = []

            for item in info_extracted.date_sheet:
                exam_dates.append(item.exam_date)
                exam_dates_subject_ordered.append(item.subject_name)

            st.session_state["subject_list"] = subject_list
            st.session_state["chapter_list"] = chapter_list
            st.session_state["exam_dates"] = exam_dates
            st.session_state["exam_dates_subjects_ordered"] = exam_dates_subject_ordered

            st.session_state["plan_generated"] = True


            day_wise_plan = day_wise_plan_chain.invoke(input={"today_date": date.today(),
                                                              "chapter_list": st.session_state["chapter_list"],
                                                              "date_sheet": st.session_state["exam_dates_subjects_ordered"],
                                                              "hours": st.session_state.user["study_hours"],
                                                              "strengths": strengths,
                                                              "views_on_syllabus": views_on_syllabus})

            st.session_state["day_wise_plan"] = day_wise_plan

            for item in day_wise_plan:
                print(item)
            st.rerun()



    else:

        if "task_counter" not in st.session_state:
            st.session_state["task_counter"] = 0

        st.title("Examination Plan")

        plan, metrics = st.tabs(["Day Wise Plan", "Chapter List and Exam Schedule"])

        with plan:

            st.subheader("Day Wise Plan")

            for day_plan in st.session_state["day_wise_plan"].daily_schedule:
                st.markdown(f"### 🗓️ {day_plan.date}")
                task_cols = st.columns(len(day_plan.tasks), width=1000)

                for i, task in enumerate(day_plan.tasks):
                    with task_cols[i]:
                        with st.container(border=True):
                            st.write(f"**{task.subject}**")
                            st.caption(f"📖 {task.chapter}")
                            st.write(task.task_description)

                st.divider()  # Adds a clean line between days


        with metrics:
            exam_date_obj = datetime.datetime.strptime(
                st.session_state["exam_dates"][0], "%d/%m/%y"
            ).date()

            days_to_exam = (exam_date_obj - date.today()).days

            metric_col1, metric_col2, metric_col3= st.columns(3)

            metric_col1.metric("Days to Exam", days_to_exam, icon="🚨", border=True, width="content")
            # metric_col2.metric("Tasks Done")
            # metric_col3.metric("Chapters Completed")

            chapter_col, date_col = st.columns(2)
            with chapter_col:
                st.subheader("Chapters")
                for i, subject in enumerate(st.session_state["chapter_list"]):
                    with st.container(border=True):
                        st.subheader(st.session_state["subject_list"][i])
                        for chapter in subject:
                            with st.container(width=1000):
                                col1, col2 = st.columns(2, gap="xxsmall")
                                with col1:
                                    st.text(chapter)
                                with col2:
                                    chapter_check = st.checkbox("Done", key=chapter)







