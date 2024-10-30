# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class BaseModel:
    """Base model with common operations"""
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

# Association table for the many-to-many relationship
student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)

class Student(db.Model, BaseModel):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Many-to-many relationship with courses
    courses = db.relationship('Course', 
                            secondary=student_courses,
                            backref=db.backref('students', lazy='dynamic'),
                            lazy='dynamic')
    
    # One-to-many relationship with queries
    queries = db.relationship('Query', backref='student', lazy=True)

    @staticmethod
    def validate_email(email):
        return email.lower()

    def __repr__(self):
        return f'<Student {self.username}>'

class Course(db.Model, BaseModel):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lecturer = db.Column(db.String(100))
    
    # One-to-many relationship with files
    files = db.relationship('File', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.code}>'

class File(db.Model, BaseModel):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_type = db.Column(db.String(50))  # lecture, assignment, resource, etc.
    
    # Relationships
    concepts = db.relationship('Concept', backref='file', lazy=True)

    def __repr__(self):
        return f'<File {self.name}>'

class Concept(db.Model, BaseModel):
    __tablename__ = 'concepts'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Concept {self.content[:30]}...>'

class Query(db.Model, BaseModel):
    __tablename__ = 'queries'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))  # Optional: link query to specific course

    def __repr__(self):
        return f'<Query {self.query[:30]}...>'