from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
mail = Mail()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')

db = SQLAlchemy(app)
Session(app)
migrate = Migrate(app, db)

def init_mail_config(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'essietasharae@gmail.com'
    app.config['MAIL_PASSWORD'] = 'aipwffszzzmzdycs'
    mail.init_app(app) 
    # A method of Flask-Mail
    # Flask-Mail extension object (mail) uses the method .init_app(app) to bind to my Flask app.
    
init_mail_config (app)  

from app import routes, models 
