from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')

db = SQLAlchemy(app)
Session(app)
migrate = Migrate(app, db)

from app import routes, models 
