from dotenv import load_dotenv
import os
import openai
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from .pdf_generator import strings

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4")

def generate_cover_letter(job_description, resume) -> str:
    class CoverLetter(BaseModel):
        intro:str
        lead_in:str
        points:list[str]
        outro:str
    
    cover_letter_template = strings.coverletter_template
    #takes {job_description} for a job description and {resume} for a resume

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", cover_letter_template)]
    )

    parser = JsonOutputParser(pydantic_object=CoverLetter)

    chain = prompt_template | model | parser

    response = chain.invoke({"job_description": job_description, "resume": resume})
    print(response)
    return response

def generate_resume_skills(job_description, resume) -> list:
    class ResumeSkill(BaseModel):
        skills: list[str]

    resume_skills_template = strings.resume_skills_template
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", resume_skills_template)]
    )

    parser = JsonOutputParser(pydantic_object=ResumeSkill)

    chain = prompt_template | model | parser

    response = chain.invoke({"job_description": job_description, "resume": resume})
    print(response)
    return response