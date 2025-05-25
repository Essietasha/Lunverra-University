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
    applicationStatus = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.hashedPassword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashedPassword, password)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registrationNumber = db.Column(db.String(10), db.ForeignKey('user.registrationNumber'))
    application_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
