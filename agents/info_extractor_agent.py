from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Dict, List

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class SubjectChapters(BaseModel):
    subject_name: str = Field(description="The name of the subject, e.g., 'Physics'")
    chapters: List[str] = Field(description="List of chapters for this specific subject")

class ExamDate(BaseModel):
    subject_name: str = Field(description="The name of the subject")
    exam_date: str = Field(description="The date of the exam")


class SyllabusDatesheetExtractor(BaseModel):
    chapter_list: List[SubjectChapters] = Field(
        description="A list containing all subjects and their extracted chapters."
    )
    date_sheet: List[ExamDate] = Field(
        description="A list containing all subjects and their corresponding exam dates."
    )


info_extractor_prompt = """
{name} is a student in Grade {grade}. He/She has his exams coming up. He/She studies {subjects}. 
His strengths are {strengths}. He/She says that {views_on_syllabus}.
Here is the extracted text from the the syllabus and datesheet pdf. 
Extract the subject wise chapter list and dates on which each exam is held based the subjects of the student.
{syllabus_datesheet_text}

"""

info_extractor_prompt_template =PromptTemplate(input_variables=["name", "grade", "subjects", "strengths", "views_on_syllabus", "syllabus_datesheet_text"], template=info_extractor_prompt)

llm_structured = llm.with_structured_output(SyllabusDatesheetExtractor)

info_extractor_chain = info_extractor_prompt_template | llm_structured