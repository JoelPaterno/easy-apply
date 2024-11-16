from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
    
    def __repr__(self):
        return f'<User({self.name!r})>'
class WorkExperience(Base):
    __tablename__ = 'workexperiences'
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    company = Column(String(500))
    location = Column(String(500))
    start_date = Column(String(500))
    end_date = Column(String(500))
    summary = Column(String(500))
    responsibil = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'))
    resume_id = Column(Integer, ForeignKey('resumes.id'))

    def __init__(self, title=None, company=None, location=None, start_date=None, end_date=None, summary=None, responsibil=None, user_id=None, resume_id=None):
        self.title = title
        self.company = company
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.summary = summary
        self.responsibil = responsibil
        self.user_id = user_id
        self.resume_id = resume_id
class Education(Base):
    __tablename__ = 'educations'
    id = Column(Integer, primary_key=True)
    degree = Column(String(500))
    institution = Column(String(500))
    location = Column(String(500))
    graduation_date = Column(String(500))
    resume_id = Column(Integer, ForeignKey('resumes.id'))

    def __init__(self, degree=None, institution=None, location=None, graduation_date=None, resume_id=None):
        self.degree = degree
        self.institution = institution
        self.location = location
        self.graduation_date = graduation_date
        self.resume_id = resume_id 
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    description = Column(String(500))
    url = Column(String(500))
    resume_id = Column(Integer, ForeignKey('resumes.id'))

    def __init__(self, title=None, description=None, url=None, resume_id=None):
        self.title = title
        self.description = description
        self.url = url
        self.resume_id = resume_id
class Certification(Base):
    __tablename__ = 'certifications'
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    issuer = Column(String(500))
    date_obtained = Column(String(500))
    resume_id = Column(Integer, ForeignKey('resumes.id'))

    def __init__(self, title=None, issuer=None, date_obtained=None, resume_id=None):
        self.title = title
        self.issuer = issuer
        self.date_obtained = date_obtained
        self.resume_id = resume_id

class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True)
    summary = Column(String(500))
    link = Column(String(100))
    skills = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'))
    workexperiences = relationship(WorkExperience, cascade="all, delete", backref="resume")
    educations = relationship(Education, cascade="all, delete", backref="resume")
    certifications = relationship(Certification, cascade="all, delete", backref="resume")
    projects = relationship(Project, cascade="all, delete", backref="resume")

    def __init__(self, summary=None, link=None, skills=None, user_id=None):
        self.summary=summary
        self.link=link
        self.skills=skills
        self.user_id=user_id
    def __repr__(self):
        return f'<Resume(user_id = {self.user_id}, summary = {self.summary}, link = {self.link}, skills = {self.skills})>'
class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    role = Column(String(500))
    company = Column(String(500))
    location = Column(String(500))
    description = Column(Text)
    link = Column(String(500)) 
    cover_letter_file_path = Column(String(500)) 
    cover_letter_data = Column(Text) 
    resume_file_path = Column(String(500)) 
    resume_data = Column(Text) 
    user_id = Column(Integer, ForeignKey('users.id'))
    resume_id = Column(Integer, ForeignKey('resumes.id'))

    def __init__(self, role=None, link=None, location=None, company=None, description=None, user_id=None, resume_id=None):
        self.role = role
        self.link = link
        self.description = description
        self.location = location
        self.company = company
        self.user_id = user_id
        self.resume_id = resume_id
    def __repr__(self):
        return f"<Application(user_id = {self.user_id}, resume_id = {self.resume_id}, role = {self.role}), description = {self.description}>"
