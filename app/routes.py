from flask import render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from datetime import datetime, timezone


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/courseInformation")
def courseInformation():
    return render_template("courseinformation.html")

@app.route("/academics")
def academics():
    return render_template("academics.html")

@app.route("/admission")
def admission():
    return render_template("admission.html")

@app.route("/application")
def application():
    return render_template("application.html")

@app.route("/campuslife")
def campuslife():
    return render_template("campuslife.html")

@app.route("/courseinformation")
def courseinformation():
    return render_template("courseinformation.html")

@app.route("/informationcentre")
def informationcentre():
    return render_template("informationcentre.html")

@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")

@app.route("/studentfinancialservices")
def studentfinancialservices():
    return render_template("sfs.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/campussafety")
def campussafety():
    return render_template("campussafety.html")

@app.route("/communications")
def communications():
    return render_template("communications.html")

@app.route("/employment")
def employment():
    return render_template("employments.html")

@app.route("/faqs")
def faqs():
    return render_template("faqs.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return render_template("logout.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")