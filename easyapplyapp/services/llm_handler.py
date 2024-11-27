from dotenv import load_dotenv
import os
import openai
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from easyapplyapp.services import strings

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4")

def create_job_application(description: str) -> dict:
    class JobApplication(BaseModel):
        role: str
        company: str
        location: str
        summary: str
    
    application_template = strings.description_application
    try:
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", application_template)]
        )

        parser = JsonOutputParser(pydantic_object=JobApplication)

        chain = prompt_template | model | parser

        response = chain.invoke({"job_description": description})
        print("CREATE JOB APPLICATION RESPONSE -- " + str(response))
        return response
    except Exception as e:
        print(e)

def generate_cover_letter(job_description: str, resume: str) -> str:
    class CoverLetter(BaseModel):
        intro:str
        lead_in:str
        points:list[str]
        outro:str
    
    cover_letter_template = strings.coverletter_template
    
    try:
        #takes {job_description} for a job description and {resume} for a resume

        prompt_template = ChatPromptTemplate.from_messages(
            [("system", cover_letter_template)]
        )

        parser = JsonOutputParser(pydantic_object=CoverLetter)

        chain = prompt_template | model | parser

        response = chain.invoke({"job_description": job_description, "resume": resume})
        #print("CREATE COVER LETTER RESPONSE -- " + str(response))
        return response
    except Exception as e:
        print(e)

def generate_resume_skills(job_description, resume) -> list:
    class ResumeSkill(BaseModel):
        skills: list[str]

    try:
        resume_skills_template = strings.resume_skills_template
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", resume_skills_template)]
        )

        parser = JsonOutputParser(pydantic_object=ResumeSkill)

        chain = prompt_template | model | parser

        response = chain.invoke({"job_description": job_description, "resume": resume})
        #print("CREATE RESUME RESPONSE -- " + str(response))
        return response
    except Exception as e:
        print(e)