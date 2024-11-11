from sqlalchemy import Column, Integer, String, ForeignKey
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


class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True)
    summary = Column(String(500))
    link = Column(String(100))
    work_experience = Column(String(500))
    skills = Column(String(500))
    education = Column(String(500))
    projects = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, summary=None, link=None, work_experience=None, skills=None, education=None, projects=None, user_id=None):
        self.summary=summary
        self.link=link
        self.work_experience=work_experience
        self.skills=skills
        self.education=education
        self.projects=projects
        self.user_id=user_id
    def __repr__(self):
        return f'<Resume(user_id = {self.user_id}, summary = {self.summary}, link = {self.link}, work_experience = {self.work_experience}, skills = {self.skills}, education = {self.eduaction}, projects = {self.projects})>'

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    role = Column(String(500))
    description = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'))
    resume_id = Column(Integer, ForeignKey('resumes.id'))

    def __init__(self, role=None, description=None, user_id=None, resume_id=None):
        self.role = role
        self.description = description
        self.user_id = user_id
        self.resume_id = resume_id
    def __repr__(self):
        return f"<Application(user_id = {self.user_id}, resume_id = {self.resume_id}, role = {self.role}), description = {self.description}>"
