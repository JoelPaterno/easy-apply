from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from werkzeug.exceptions import abort
from .auth import login_required
from .db import db_session
from .models import Resume, User, WorkExperience
from sqlalchemy import update

bp = Blueprint('profile', __name__)

@bp.route('/')
def index():
    cur_user_id = session.get('user_id')
    user = User.query.filter(User.id == cur_user_id).first()
    resumes = Resume.query.filter(Resume.user_id == cur_user_id).all()
    workexperiences_result = []
    for resume in resumes:
        print(resume.id)
        workexperiences = WorkExperience.query.filter(WorkExperience.resume_id == resume.id).all()
        for workexperience in workexperiences:
            workexperiences_result.append(workexperience)
    return render_template('app/index.html', user=user, resumes=resumes, workexperiences_result=workexperiences_result)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        summary = request.form['summary']
        link = request.form['link']
        skills = request.form['skills']
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        start_date = request.form['start']
        end_date = request.form['end']
        job_summary = request.form['job-summary']
        responsibil = request.form['responsibilities']
        error = None

        if not summary:
            error = "summary is required"
        
        if error is not None:
            flash(error)
        else:
            try:
                resume = Resume(summary=summary, link=link, skills=skills, user_id=session.get('user_id'))
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
                db_session.add(workexperience)
                db_session.commit()
            except:
                flash("unable to ass work experience to the database")
            return redirect(url_for('profile.index'))   
    return render_template('app/create.html')

def get_resume(id, check_author=True):
    resume = Resume.query.filter(Resume.id == id).first()
    print(f"Resume: id = {resume.id} user_id = {resume.user_id} summary = {resume.summary}")
    print(f"Session user id : {session.get('user_id')}")

    if resume is None:
        abort(404, f"resume {id} doesn't exist")
    if check_author and resume.user_id != session.get('user_id'):
        abort(403)
    return resume


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
    if request.method == 'POST':
        pass
    return render_template('app/apply.html')