from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registrationNumber = db.Column(db.String(10), unique=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    hashedPassword = db.Column(db.String(200))
    dob = db.Column(db.Date)
    phone = db.Column(db.String(100))
    program = db.Column(db.String(100))
    intake = db.Column(db.String(100))
    edubackground = db.Column(db.String(200))
    addMessage = db.Column(db.String(200))
    is_approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_registered = db.Column(db.Boolean, default=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    faculty = db.relationship('Faculty', backref='students')
    department = db.relationship('Department', backref='students')
    
    def set_password(self, password):
        self.hashedPassword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashedPassword, password)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registrationNumber = db.Column(db.String(10), db.ForeignKey('user.registrationNumber'))
    application_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = db.relationship('User', backref='applications')

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    departments = db.relationship('Department', backref='faculty', lazy=True)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    facultyID = db.Column(db.Integer, db.ForeignKey('faculty.id'))

    courses = db.relationship('Course', backref='department', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(10), unique=True)
    departmentID = db.Column(db.Integer, db.ForeignKey('department.id'))

class CourseRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    courseID = db.Column(db.Integer, db.ForeignKey('course.id'))
    registeredAT = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    course = db.relationship('Course', backref='registrations')

