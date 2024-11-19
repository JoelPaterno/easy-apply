from flask import Blueprint, flash, redirect, render_template, request, url_for, session, send_from_directory
from werkzeug.exceptions import abort
from .auth import login_required
from .db import db_session
from .models import Resume, User, WorkExperience, Application, Education, Certification, Project
from easyapplyapp.services import llm_handler
from easyapplyapp.services.pdf_generator import generate_cover_letter, generate_resume
import json
import os

bp = Blueprint('profile', __name__)

@bp.route('/')
@login_required
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

def extract_num(key : str) -> int: 
    count_str = ""
    for num in range(len(key)):
        if key[num].isnumeric():
            count_str += str(key[num])
    count = int(count_str)
    return count

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    cur_user_id = session.get('user_id')
    user = User.query.filter(User.id == cur_user_id).first()
    if request.method == 'POST':
        #TODO: the incoming post data will be dynamic based on how many additions were made this will be parsed into a python dict. 
        #which will then be used to populate the database objects and commit the resume to the db.
         
        #for testing form request for dynamically added sections
        print(request.headers)
        fields = [k for k in request.form]
        values = [request.form[k] for k in request.form]
        data = dict(zip(fields, values))
        print(data)

        #loop through data to populate counts - need to update names of fields to correspond to objects
        #"WE1" WE code for work experience followed by count. 
        weCount = 0
        edCount = 0
        certCount = 0
        projCount = 0

        for key in fields:
            #slice list to look for object code
            sliced = key[:2]
            if sliced == "WE":
                weCount = extract_num(key)
            elif sliced == "ED":
                edCount = extract_num(key)
            elif sliced == "CT":
                certCount = extract_num(key)
            elif sliced == "PJ":
                projCount = extract_num(key)

        print("we count = "+ str(weCount))
        print("ed count = "+ str(edCount))
        print("cert count = "+ str(certCount))
        print("proj count = "+ str(projCount))

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        summary = request.form['summary']
        link = request.form['link']
        skills = request.form['skills']

        error = None
        
        if error is not None:
            flash(error)
        else:
            try:
                resume = Resume(name=name, phone=phone, address=address, email=email, summary=summary, link=link, skills=skills, user_id=cur_user_id)
                db_session.add(resume)
                db_session.flush()
                #Handle Work Experience
                for i in range(1, weCount + 1):
                    k = "WE" + str(i)
                    we_title = request.form[k + "title"]
                    we_company = request.form[k + "company"]
                    we_location = request.form[k + "location"]
                    we_start = request.form[k + "startdate"]
                    we_end = request.form[k + "enddate"]
                    we_responsibil = request.form[k + "responsibil"]
                    we_summary = request.form[k + "summary"]
                    #add to db
                    workexperience = WorkExperience(
                            title=we_title,
                            company=we_company,
                            location=we_location,
                            start_date=we_start,
                            end_date=we_end,
                            responsibil=we_responsibil,
                            summary=we_summary,
                            user_id=session.get('user_id'),
                            resume_id=resume.id,
                        )
                    db_session.add(workexperience)
                #Handle Education
                for i in range(1, edCount + 1):
                    k = "ED" + str(i)
                    ed_institution = request.form[k + "institution"]
                    ed_location = request.form[k + "location"]
                    ed_date = request.form[k + "date"]
                    ed_degree = request.form[k + "degree"]
                    #add to db
                    education = Education(
                            institution=ed_institution,
                            location=ed_location,
                            graduation_date=ed_date,
                            degree=ed_degree,
                            resume_id=resume.id,
                        ) 
                    db_session.add(education)
                #Handle Projects
                for i in range(1, certCount + 1):
                    k = "CT" + str(i) 
                    ct_title = request.form[k + "title"]
                    ct_issuer = request.form[k + "issuer"]
                    ct_date = request.form[k + "date"]
                    #add to db
                    cert = Certification(
                            title=ct_title,
                            issuer=ct_issuer,
                            date_obtained=ct_date,
                            resume_id=resume.id,
                        )
                    db_session.add(cert)
                    
                #Handle Certifications
                for i in range(1, projCount + 1):
                    k = "PJ" + str(i)
                    pj_title = request.form[k + "title"]
                    pj_desc = request.form[k + "description"]
                    pj_url = request.form[k + "url"]
                    pj_date = request.form[k + "date"]
                    #add to db
                    project = Project(
                            title=pj_title,
                            description=pj_desc,
                            url=pj_url,
                            resume_id=resume.id,
                        )
                    db_session.add(project)
                db_session.commit()
            except Exception as e:
                flash("unable to add resume data to the database")
                print(e)
            return redirect(url_for('profile.index'))   
    return render_template('app/create.html', user=user)

def get_resume(id, check_author=True):
    resume = Resume.query.filter(Resume.id == id).first()
    #print(f"Resume: id = {resume.id} user_id = {resume.user_id} summary = {resume.summary}")
    #print(f"Session user id : {session.get('user_id')}")

    if resume is None:
        abort(404, f"resume {id} doesn't exist")
    if check_author and resume.user_id != session.get('user_id'):
        abort(403)
    return resume

def resume_serializer(id: int) -> dict:
    """
    Will make database queries and serialise the data to create a python dict of the resume data for a user. 
    params = resume(id)
    returns = resume(dict)
    """
    resume = get_resume(id)
    user = User.query.filter(User.id == resume.user_id).first()
    resume_dict = {
        'name': resume.name,
        'email': resume.email,
        'phone': resume.phone,
        'address': resume.address,
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
            "location": we.location,
            "startDate": we.start_date,
            "endDate": we.end_date,
            "summary": we.summary,
            "responsibilities": we.responsibil.split(", ")
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

    #print(f"SERIALISED RESUME DATA DICT - {resume_dict}")
    return resume_dict
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    
    #print(f"requested resume id: {id}")
    user = User.query.filter(User.id == session.get("user_id")).first()
    resume = get_resume(id)
    workexperiences = WorkExperience.query.filter(WorkExperience.resume_id == resume.id).all()
    certifications = Certification.query.filter(Certification.resume_id == resume.id).all()
    educations = Education.query.filter(Education.resume_id == resume.id).all()
    projects = Project.query.filter(Project.resume_id == resume.id).all()
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
    return render_template(
        'app/update.html', 
        user=user,
        resume=resume, 
        workexperiences=workexperiences,
        certifications=certifications,
        educations=educations,
        projects=projects,
        )

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

        try:
            application_data = llm_handler.create_job_application(description)
        except Exception as e:
            print(e)
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
    resume = Resume.query.filter(Resume.user_id == session.get("user_id")).first()
    cwd = os.getcwd()

    if application.resume_data is None:
        #TODO: Modify this to call resume_serialiser() with the first resume. a resume data dict will be returned which can then be used the same as the loaded json file.
        resume_data = resume_serializer(resume.id)
        print("RESUME DATA LOADED IN FOR LLM BY SERIALISER - " + json.dumps(resume_data))
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
        #get these details from the selected resume. 
        cover_letter['name'] = resume_data['name']
        cover_letter['email'] = resume_data['email']
        cover_letter['phone'] = resume_data['phone']
        cover_letter['address'] = resume_data['address']
        cover_letter['website'] = resume_data['website_link']
        cover_letter['saultation'] = "Dear Hiring Manager"
        cover_letter['signature'] = "Sincerely,"
        print(cover_letter)
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

@bp.route('/<int:id>/updateapp', methods=('POST', 'GET'))
@login_required
def update_application(id):
    application = Application.query.filter(Application.id == id).first()
    cover_letter_data = json.loads(application.cover_letter_data)
    resume_data = json.loads(application.resume_data)
    resume_skills = enumerate(resume_data['skills'])
    cover_letter_data['points'] = enumerate(cover_letter_data['points'])
    if request.method == 'POST':
        #print(request.headers)
        fields = [k for k in request.form]
        values = [request.form[k] for k in request.form]
        data = dict(zip(fields, values))
        print(data)

        skillCount = 0
        pointsCount = 0

        for key in fields:
            check = key[:5]
            sliced = key[5:]
            if check == "skill" and int(sliced) > skillCount:
                skillCount = int(sliced)
            elif check == "point" and int(sliced) > pointsCount:
                pointsCount = int(sliced)

        skills = []
        points = []
        #TODO: loop through skills and points and populate
        for skill in range(skillCount):
            print(request.form['skill'+str(skill)])
            skills.append(request.form['skill'+str(skill)])
        for point in range(pointsCount + 1):
            print(request.form['point'+str(point)])
            points.append(request.form['point'+str(point)])
        #print("Skills  -- " + str(list(skills)))
        #print("cl points -- " + str(list(points)))
        #parse skills
        resume_data['skills'] = skills
        cover_letter_data['intro'] = request.form['intro']
        cover_letter_data['lead_in'] = request.form['lead_in']
        #parse points
        cover_letter_data['points'] = points
        cover_letter_data['outro'] = request.form['outro']
        #edit cover letter data and resume skills
        application.resume_data = json.dumps(resume_data)
        #print("EDITING RESUME DATA TO - " + json.dumps(resume_data))
        application.cover_letter_data = json.dumps(cover_letter_data)
        #print("EDITING CL DATA TO - " + json.dumps(cover_letter_data))
        db_session.commit()
        regenerate(id=application.id)
        return redirect(url_for('profile.update_application' , id=id))

    with open(application.resume_file_path, "r") as resume:
        resume_html = resume.read()
    
    with open(application.cover_letter_file_path) as cl:
        coverletter_html = cl.read()

    return render_template(
        'app/update_application.html', 
        application=application, 
        cover_letter_data=cover_letter_data, 
        resume_skills=resume_skills,
        resume_html=resume_html,
        coverletter_html=coverletter_html,
        )

@bp.route('/<int:id>/deleteapp', methods=('POST',))
@login_required
def delete_app(id):
    application = Application.query.filter(Application.id == id).first()
    db_session.delete(application)
    db_session.commit()
    return redirect(url_for('profile.apply'))


@bp.route('/<int:id>/regenrate', methods=('GET',))
@login_required
def regenerate(id):
    application = Application.query.filter(Application.id == id).first()
    cwd = os.getcwd()
    #get data for cl and resume
    resume_data = json.loads(application.resume_data)
    #parse skills string
    #print(resume_data['skills'])
    #print(json.dumps(resume_data, indent=2))


    cover_letter = json.loads(application.cover_letter_data)
    #parse points string
    #print(cover_letter['points'])
    #print(json.dumps(cover_letter, indent=2))

    #call pdf generate functions
    if os.path.exists(application.resume_file_path):
        os.remove(application.resume_file_path)
        print("resume file deleted")
    else:
        print("file not deleted -- the file does not exists")
    resume_path = generate_resume(resume_data=resume_data, appfilepath=cwd)
    application.resume_file_path = resume_path

    if os.path.exists(application.cover_letter_file_path):
        os.remove(application.cover_letter_file_path)
        print("cover_letter file deleted")
    else:
        print("file not deleted -- the file does not exists")
    cover_letter_path = generate_cover_letter(cover_letter_dict=cover_letter, appfilepath=cwd)
    application.cover_letter_file_path = cover_letter_path

    db_session.commit()
    return redirect(url_for('profile.apply'))

@bp.route('/<int:id>/resumedl', methods=('GET',))
@login_required
def resume_dl(id):
    application = Application.query.filter(Application.id == id).first()
    cwd = os.getcwd()
    resume_folder = os.path.join(cwd, 'easyapplyapp', 'files', 'resumes')
    resume_filename = application.resume_file_path[-25:]
    #print(resume_filename)
    return send_from_directory(resume_folder, resume_filename, as_attachment=True)

@bp.route('/<int:id>/coverletterdl', methods=('GET',))
@login_required
def coverletter_dl(id):
    application = Application.query.filter(Application.id == id).first()
    cwd = os.getcwd()
    coverletter_folder = os.path.join(cwd, 'easyapplyapp', 'files', 'coverletters')
    coverletter_filename = application.cover_letter_file_path[-25:]
    #print(coverletter_filename)
    return send_from_directory(coverletter_folder, coverletter_filename, as_attachment=True)


