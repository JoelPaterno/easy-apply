import jinja2
import pdfkit
from datetime import datetime
import json
import llm_handler

def generate_cover_letter(job_description, company_name, job_title):
    """
    This function takes data to be passed to the llm handler and generates a cover letter.:
    - all the resume data as json
    - all of the job data in a string
    """
    #TODO: change this to be a database query of all resume data for the user
    with open('pdf_generator/resume_data.json') as f:
            resume_data = json.load(f)

    #TODO: change this to be a database query of all cover_letter data for the user
    with open('pdf_generator/cover_letter_data.json') as f:
            cover_letter_data = json.load(f)

    resume_data_str = json.dumps(resume_data)
    cover_letter = llm_handler.generate_cover_letter(job_description, resume_data_str)
    today_date = datetime.today().strftime('%d/%m/%Y')

    cover_letter_data["intro"] = cover_letter["intro"]
    cover_letter_data["lead_in"] = cover_letter["lead_in"]
    cover_letter_data["points"] = cover_letter["points"]
    cover_letter_data["outro"] = cover_letter["outro"]
    
    content = cover_letter_data
    content["current_date"] = today_date

    template_loader = jinja2.FileSystemLoader('.easyapplyapp\\services\\templates')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('cover_letter_template_1.html')
    output_text = template.render(content)

    config = pdfkit.configuration(wkhtmltopdf='.wkhtmltopdf.exe')
    try:
        pdfkit.from_string(
                output_text, f'.easyapplyapp\\files\\coverletters\\{job_title} {company_name} Cover Letter.pdf', 
                configuration=config, 
                css=".easyapplyapp\services\styles\cover_letter_template_1_styles.css"
                )
    except:
        print("Unable to generate cover letter pdf")

def generate_resume(job_description,title, company):
    today_date = datetime.today().strftime('%d %b, %Y')
    
    #TODO: change this to be a database query of all resume data for the user
    with open('pdf_generator/resume_data.json') as f:
            resume_data = json.load(f)

    content = resume_data

    #update skills with chat gpt call
    skills = llm_handler.generate_resume_skills(job_description, resume_data)
    content["skills"] = skills

    template_loader = jinja2.FileSystemLoader('.easyapplyapp\\services\\templates')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('resume_template_1.html')
    output_text = template.render(content)

    config = pdfkit.configuration(wkhtmltopdf='.wkhtmltopdf.exe')
    try:    
        pdfkit.from_string(
            output_text, f'.easyapplyapp\\files\\resumes\\{title} {company} Resume.pdf', 
            configuration=config,
            css=".easyapplyapp\\services\\styles\\resume_template_1_style.css",
            )
    except:
        print("Unable to create resume")