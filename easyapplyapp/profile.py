from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from werkzeug.exceptions import abort
from .auth import login_required
from .db import db_session
from .models import Resume, User, WorkExperience, Application, Education, Certification, Project
from sqlalchemy import update
from easyapplyapp.services import llm_handler
from easyapplyapp.services.pdf_generator import generate_cover_letter, generate_resume, generate_filename
import json
import os

bp = Blueprint('profile', __name__)

@bp.route('/')
def index():
    cur_user_id = session.get('user_id')
    user = User.query.filter(User.id == cur_user_id).first()
    resumes = Resume.query.filter(Resume.user_id == cur_user_id).all()
    workexperiences_result = []
    for resume in resumes:
        workexperiences = WorkExperience.query.filter(WorkExperience.resume_id == resume.id).all()
        for workexperience in workexperiences:
            workexperiences_result.append(workexperience)
    return render_template('app/index.html', user=user, resumes=resumes, workexperiences_result=workexperiences_result)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    cur_user_id = session.get('user_id')
    user = User.query.filter(User.id == cur_user_id).first()
    if request.method == 'POST':
        #for testing form request for dynamically added sections
        print(request.headers)
        fields = [k for k in request.form]
        values = [request.form[k] for k in request.form]
        data = dict(zip(fields, values))
        print(data)

        summary = request.form['summary']
        link = request.form['link']
        skills = request.form['skills']
        #Handle Work Experience
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        start_date = request.form['start']
        end_date = request.form['end']
        job_summary = request.form['job-summary']
        responsibil = request.form['responsibilities']
        error = None
        #Handle Education
        degree = request.form['degree']
        institution = request.form['institution']
        education_location = request.form['education_location']
        graduation_date = request.form['graduation_date']
        #Handle Projects
        project_title = request.form['project_title']
        project_description = request.form['project_description']
        project_url = request.form['project_url']
        #Handle Certifications
        cert_title = request.form['cert_title']
        issuer = request.form['issuer']
        date_obtained = request.form['date_obtained']

        if not summary:
            error = "summary is required"
        
        if error is not None:
            flash(error)
        else:
            try:
                resume = Resume(summary=summary, link=link, skills=skills, user_id=cur_user_id)
                db_session.add(resume)
                db_session.flush()
                workexperience = WorkExperience(
                    title=title, 
                    company=company, 
                    location=location, 
                    start_date=start_date,
                    end_date=end_date,
                    summary=job_summary,
                    responsibil=responsibil,
                    user_id=session.get('user_id'),
                    resume_id=resume.id,
                    )
                education = Education(
                    degree=degree,
                    institution=institution,
                    location=education_location,
                    graduation_date=graduation_date, 
                    resume_id=resume.id,
                ) 
                project = Project(
                    title=project_title,
                    description=project_description,
                    url=project_url,
                    resume_id=resume.id,
                )
                cert = Certification(
                    title=cert_title,
                    issuer=issuer,
                    date_obtained=date_obtained,
                    resume_id=resume.id,
                )
                db_session.add(workexperience)
                db_session.add(education)
                db_session.add(project)
                db_session.add(cert)
                db_session.commit()
            except:
                flash("unable to add resume data to the database")
            return redirect(url_for('profile.index'))   
    return render_template('app/create.html', user=user)

def get_resume(id, check_author=True):
    resume = Resume.query.filter(Resume.id == id).first()
    print(f"Resume: id = {resume.id} user_id = {resume.user_id} summary = {resume.summary}")
    print(f"Session user id : {session.get('user_id')}")

    if resume is None:
        abort(404, f"resume {id} doesn't exist")
    if check_author and resume.user_id != session.get('user_id'):
        abort(403)
    return resume

def resume_serializer(id: int) -> dict:
    """
    Will make database queries and serialise the data to create a python dict of the resume data for a user. 
    """
    resume = get_resume(id)
    user = User.query.filter(User.id == resume.user_id).first()
    resume_dict = {
        'name': user.name,
        'email': '',
        'phone': '',
        'address': '',
        'website_link': resume.link,
        'summary': resume.summary,
        'education': [],
        'work_experience': [],
        'skills': [],
        'projects': [],
        'certifications': [],
    }

    resume_skills = resume.skills.split(", ")
    resume_dict['skills'] = resume_skills

    #initaially only one of each
    educations = Education.query.filter(Education.resume_id == id)
    for ed in educations:
        education_dict = {
            "degree": ed.degree,
            "institution": ed.institution,
            "location": ed.location,
            "graduationDate": ed.graduation_date
        }
        resume_dict['education'].append(education_dict)

    work_experiences = WorkExperience.query.filter(WorkExperience.resume_id == id)
    for we in work_experiences:
        work_experience_dict = {
            "title": we.title,
            "company": we.company,
            "location": we.company,
            "startDate": we.company,
            "endDate": we.company,
            "summary": we.company,
            "responsibilities": [we.responsibil.split(", ")]
        }
        resume_dict['work_experience'].append(work_experience_dict)

    projects = Project.query.filter(Project.resume_id == id)
    for proj in projects:
        project_dict = {
            "name": proj.title,
            "description": proj.description,
            "url": proj.url
        }
        resume_dict['projects'].append(project_dict)

    certifications = Certification.query.filter(Certification.resume_id == id)
    for cert in certifications:
        cert_dict = {
            "name": cert.title,
            "issuer": cert.issuer,
            "dateObtained": cert.date_obtained
        }
        resume_dict['certifications'].append(cert_dict)

    print(f"SERIALISED RESUME DATA - {resume_dict}")
    return resume_dict



@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    print(f"requested resume id: {id}")
    resume = get_resume(id)

    if request.method == 'POST':
        summary = request.form['summary']
        link = request.form['link']
        skills = request.form['skills']
        error = None

        if not summary:
            error = "summary is required"

        if error is not None:
            flash(error)
        else: 
            resume.summary = summary
            resume.link = link
            resume.skills = skills
            db_session.commit()
            return redirect(url_for('profile.index'))
    return render_template('app/update.html', resume=resume)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def deleted(id):
    resume = get_resume(id)
    db_session.delete(resume)
    db_session.commit()
    return redirect(url_for('profile.index'))

@bp.route('/apply', methods=('GET', 'POST'))
@login_required
def apply():
    cur_user_id = session.get("user_id")
    user = User.query.filter(User.id == cur_user_id).first()
    applications = Application.query.filter(Application.user_id == cur_user_id)
    #currently no selection of resume at job application stage
    resume = Resume.query.filter(Resume.user_id == cur_user_id).first()
    if request.method == 'POST':
        link = request.form['link']
        description = request.form['paste']

        #TODO llm function create_job_application(description) will take the description and provide strucured data to create a job application object to add to db
        application_data = llm_handler.create_job_application(description)
        role = application_data['role']
        location = application_data['location']
        company = application_data['company']
        error = None

        if not description:
            error = "description is required"
        
        if error is not None:
            flash(error)
        else:
            try:
                application = Application(role=role, link=link, description=description, location=location, company=company, user_id=cur_user_id, resume_id=resume.id)
                db_session.add(application)
                db_session.commit()
            except Exception as error:
                flash("An Error Occured:", error)
        return redirect(url_for('profile.apply'))  
    return render_template('app/apply.html', user=user, applications=applications, resume=resume)

@bp.route('/<int:id>/start', methods=('POST', 'GET'))
@login_required
def start_application(id):
    #get application
    application = Application.query.filter(Application.id == id).first()
    #load in resume data from the json file
    cwd = os.getcwd()
    json_path = os.path.join(cwd, 'easyapplyapp','services', 'resume_data.json')

    if application.resume_data is None:
        try:
            with open(json_path) as f:
                    resume_data = json.load(f)
        except Exception as e:
            print(e)
        finally:
            "Unknown error start route"
    else: 
        resume_data = json.loads(application.resume_data)
    #call llm handler generate_resume_skills -> list of skills
    resume_str = json.dumps(resume_data)
    if application.resume_data is None:
        resume_skills = llm_handler.generate_resume_skills(job_description=application.description, resume=resume_str)
        resume_data['skills'] = resume_skills
        resume_data_str = json.dumps(resume_data)
        application.resume_data = resume_data_str
    
    #call llm handler generate_cover_letter -> dict cover letter. 
    if application.cover_letter_data is None:
        cover_letter = llm_handler.generate_cover_letter(job_description=application.description, resume=resume_data_str)
        application.cover_letter_data = json.dumps(cover_letter)
    else:
        cover_letter = json.loads(application.cover_letter_data)
    
    #call pdf_generator to create resume html file -> application(res_path and res_data) and resume.html file
    if application.resume_file_path is None:
        resume_path = generate_resume(resume_data=resume_data, appfilepath=cwd)
        application.resume_file_path = resume_path
    #call pdf_generator to create cover letter html file -> application(cl_path and cl_data) and cover_letter.html file
    if application.cover_letter_file_path is None:
        cover_letter_path = generate_cover_letter(cover_letter_dict=cover_letter, appfilepath=cwd)
        application.cover_letter_file_path = cover_letter_path
    #commit changed application to the db
    db_session.commit()
    #redirect to applications
    return redirect(url_for('profile.apply'))