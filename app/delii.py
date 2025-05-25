from app import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    departments = db.relationship('Department', backref='faculty')

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    courses = db.relationship('Course', backref='department')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    credits = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))