import jinja2
import pdfkit
from datetime import datetime
import json
from easyapplyapp.services import llm_handler
from easyapplyapp.models import Application

def generate_cover_letter(application: Application, resume: dict) -> Application:
    """
    Modify to take an application object created on form submit and will populate the cover_letter_data and cover_letter_path attributes of the object
    args - Application
    return - Application
    """
    #TODO: change this to be a database query of all resume data for the user
    resume_data = resume

    #TODO: change this to be a create a cover letter cover_letter data for the user
    today_date = datetime.today().strftime('%d/%m/%Y')
    cover_letter_data = {
         'intro': '',
         'lead_in': '',
         'points': [],
         'outro': '',
         'current_date': today_date, 
    }

    resume_data_str = json.dumps(resume_data)
    cover_letter = llm_handler.generate_cover_letter(application.description, resume_data_str)

    cover_letter_data["intro"] = cover_letter["intro"]
    cover_letter_data["lead_in"] = cover_letter["lead_in"]
    cover_letter_data["points"] = cover_letter["points"]
    cover_letter_data["outro"] = cover_letter["outro"]

    application.cover_letter_data = cover_letter_data

    template_loader = jinja2.FileSystemLoader('.easyapplyapp\\services\\templates')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('cover_letter_template_1.html')
    output_text = template.render(cover_letter_data)
    output_path = f'.easyapplyapp\\files\\coverletters\\{application.role} {application.company} Cover Letter.pdf'

    config = pdfkit.configuration(wkhtmltopdf='.wkhtmltopdf.exe')
    try:
        pdfkit.from_string(
                output_text, output_path, 
                configuration=config, 
                css=".easyapplyapp\services\styles\cover_letter_template_1_styles.css"
                )
        application.cover_letter_file_path = output_path
        return application
    except:
        print("Unable to generate cover letter pdf")
        return None

def generate_resume(application: Application, resume: dict) -> Application:
    """
    Modify to take an application object created on form submit and will populate the resume_data and resume_path attributes of the object
    args - Application
    return - Application
    """

    today_date = datetime.today().strftime('%d %b, %Y')
    
    #TODO: change this to be a database query of all resume data for the user
    #resume_serializer()
    resume_data = resume

    #update skills with chat gpt call
    skills = llm_handler.generate_resume_skills(application.description, resume_data)
    resume_data["skills"] = skills
    application.resume_data = resume_data

    template_loader = jinja2.FileSystemLoader('.easyapplyapp\\services\\templates')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('resume_template_1.html')
    output_text = template.render(resume_data)
    output_path = f'.easyapplyapp\\files\\resumes\\{application.role} {application.company} Resume.pdf',

    config = pdfkit.configuration(wkhtmltopdf='.wkhtmltopdf.exe')
    try:    
        pdfkit.from_string(
            output_text, output_path, 
            configuration=config,
            css=".easyapplyapp\\services\\styles\\resume_template_1_style.css",
            )
        application.resume_file_path = output_path
    except:
        print("Unable to create resume")