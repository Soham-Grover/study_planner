from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Dict, List


llm = ChatOpenAI(model="gpt-4o")

class Task(BaseModel):
    subject: str = Field(description="Subject that the student has to study for that specific task. E.g. Physics")
    chapter: str = Field(description="Name of the chapter for that specific subject that we need to study. E.g. Thermodynamics")
    task_description: str = Field(description="Description of the task that the student has to do while studying that chapter")
    time: str = Field(description="Estimate time take for that task")

class DayPlan(BaseModel):
    tasks: List[Task] = Field(description="A list of tasks that the student has to do for that specific day. One day can have a maximum of 4 tasks")
    date: str = Field(description="Date of the task and when to do it. Should be in the format: Day of the week, DD Month")

class DayWisePlan(BaseModel):
    daily_schedule: List[DayPlan] = Field(description="Day-to-Day plan for the preparation of the upcoming exams")

day_wise_plan_prompt = """
You are a professional academic tutor. Create a detailed day-wise study plan for a student whose exams are around the corner up till the date of the first exam. 
Inputs:
- Date of plan creation (Today): {today_date}
- Chapters along with subjects: {chapter_list}
- Date sheet of the exams: {date_sheet}
- Number of hours the student devotes to studying per day besides school: {hours}
- Strength of the student: {strengths}
- Views of the student: {views_on_syllabus}

IMPORTANT POINT TO TAKE CARE OF:
1. Make the plan so that all the topics of the chapters are spaced properly in the given time frame and the plan must contain exactly the number of days from today to the date of the first exam.
2. For each day, there can be a maximum of 4 tasks
3. Once all chapters are covered, you schedule test and revision times."""

day_wise_plan_prompt_template = PromptTemplate(input_variables=["today_date","chapter_list", "date_sheet", "hours", "strengths", "views_on_syllabus"], template=day_wise_plan_prompt)

llm_structured = llm.with_structured_output(DayWisePlan)

day_wise_plan_chain = day_wise_plan_prompt_template | llm_structured

