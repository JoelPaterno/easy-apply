import jinja2
import pdfkit
from datetime import datetime
import os
from easyapplyapp.services import llm_handler
from easyapplyapp.models import Application
import random
import string

def generate_filename():
     chars = string.ascii_lowercase + string.digits
     filename = ''.join(random.choice(chars) for _ in range(20))
     #TODO: check if it already exists
     return filename
     
def generate_cover_letter(cover_letter_dict: dict, appfilepath=None) -> str:
    """
    Modify to take an application object created on form submit and will populate the cover_letter_data and cover_letter_path attributes of the object
    args - dict of cl data
    return - path to generated file
    """
    filename = generate_filename()

    #TODO: Generate resume.html file
    template_loader = jinja2.FileSystemLoader(os.path.join(appfilepath, 'easyapplyapp', 'services', 'templates'))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('cover_letter_template_1.html')
    output_text = template.render(cover_letter_dict)
    output_path = os.path.join(appfilepath, 'easyapplyapp', 'files', 'coverletters')
    try:
        os.chdir(output_path)
        with open(f'{filename}.html', 'w') as f:
                f.write(output_text)
        os.chdir(appfilepath)
        print("FILE GENERATED TO COVER LETTER-- " + output_path + '\\' + f'{filename}.html')
        return os.path.join(output_path, f'{filename}.html')
    except Exception as e:
         print(e)
    finally: 
         "Unknown error pdf_generator generate_cover_letter()"


def generate_resume(resume_data: dict, appfilepath=None) -> str:
    """
    Modify to take an application object created on form submit and will populate the resume_data and resume_path attributes of the object
    args - string of the resume data
    return - path to generated file
    """
    filename = generate_filename()

    #TODO: Generate resume.html file
    template_loader = jinja2.FileSystemLoader(os.path.join(appfilepath, 'easyapplyapp', 'services', 'templates'))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('resume_template_1.html')
    output_text = template.render(resume_data)
    output_path = os.path.join(appfilepath, 'easyapplyapp', 'files', 'resumes')
    try:
        os.chdir(output_path)
        with open(f'{filename}.html', 'w') as f:
                f.write(output_text)
        os.chdir(appfilepath)
        print("FILE GENERATED TO RESUME -- " + output_path + '\\' + f'{filename}.html')
        return os.path.join(output_path, f'{filename}.html')
    except Exception as e:
         print(e)
    finally: 
         "Unknown error pdf_generator generate_resume()"
    
