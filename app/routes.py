from flask import render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
import re, bleach, random
from app.helpers import login_required
from datetime import datetime, timezone
from app.models import User, Application
from app.email import send_studentID, send_applicationConfirmation

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

def validate_input(input_str):
    pattern = r"^[A-Za-z0-9.,!+\-?'@#&’\";:\s]+$"
    if not re.match(pattern, input_str):
        raise ValueError("Invalid input. Only alphabets, numbers, and .,!?@#&'\";: are allowed.")
    return input_str


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
    if not re.match(pattern, password):
        raise ValueError(
            "Password must be at least 8 characters long, include an uppercase letter, "
            "a lowercase letter, a digit, and a special character."
        )
    return password


def sanitize_input(input_str):
    return bleach.clean(input_str, tags=[], attributes={}, strip=True)


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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "userID" in session:
        session.clear()

    if request.method == "POST":
        username = request.form.get("firstname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        if not username or not email or not password or not confirmpassword:
            flash("Please fill out all fields!", "danger")
            return redirect("/signup")
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.", "danger")
            return redirect("/signup")
        
        if password != confirmpassword:
            flash("Passwords don't match!", "danger")
            return redirect("/signup")
        
        if len(firstname) < 3:
            flash("Name must be at least 3 characters!", "danger")
            return redirect("/signup")
        
        if len(password) < 8:
            flash("Password must be at least 8 charcaters!", "danger")
            return redirect("/signup")

        try:
            firstname = sanitize_input(validate_input(firstname)).lower
            email = sanitize_input(validate_input(email))
            validate_password(password)
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/signup")
        
        existingUser = User.query.filter_by(firstname=firstname).first()
        if existingUser:
            flash(f"Oops! {firstname} exists, please try another name.", "danger")
            return redirect("/signup")
        
        password= generate_password_hash(password)
        registeredNumber = "lv" + firstname[:3].lower() + str(random.randint(10000, 99999))

        newSignUpUser = User(firstname=firstname, hashedPassword=password, email=email, registrationNumber=registeredNumber)
        db.session.add(newSignUpUser)

        try:
            db.session.commit()
        except Exception as e:
            flash(f"An error occured: {str(e)}", "danger")
            return redirect("/signup")
        
        send_studentID(email, firstname, registeredNumber)
        flash("Sign up successful! Please check your email for your STUDENT ID", "success")
        return redirect("/login")
    
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "userID" in session:
        session.clear()

    if request.method == "POST":
        regNum = request.form.get("regNum")
        password = request.form.get("password")

        if not regNum or not password:
            flash("Please enter your Registration Number and Password!", "danger")
            return redirect("/login")
        
        try:
            regNum = sanitize_input(validate_input(regNum)).lower()
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/login")
        
        user = User.query.filter_by(registrationNumber=regNum).first()

        if not user or not check_password_hash(user.hashedPassword, password):
            flash("Username or Password incorrect!", "danger")
            return redirect("/login")

        session["userID"] = user.id
        flash("Successfully Logged in.", "success")
        return redirect("/")
         
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    flash("Logged Out!", "success")
    session.pop("userID", None)
    return redirect("/")


@app.route("/application", methods=["GET", "POST"])
@login_required
def application():
    userID = session.get("userID")  

    if request.method == "POST":
        firstname = request.form.get("firstname")
        email = request.form.get("email")
        lastname = request.form.get("lastname")
        phone = request.form.get("phone")
        dob = request.form.get("dob")
        program = request.form.get("program")
        intake = request.form.get("intake")
        edubackground = request.form.get("edubackground")
        addMessage = request.form.get("addMessage")

        if not lastname or not phone or not dob or not program or not intake or not edubackground:
            flash("Please fill out all fields!", "danger")
            return redirect("/application")
        
        if (phone.startswith('+') and not phone[1:].isdigit()) or (not phone.startswith('+') and not phone.isdigit()) or len(phone) < 7:
            flash("Phone number must be numeric and have at least 7 digits.", "danger")
            return redirect("/application")        
        
        try:
            lastname = sanitize_input(validate_input(lastname))
            phone = sanitize_input(validate_input(phone))
            edubackground = sanitize_input(validate_input(edubackground))
            addMessage = sanitize_input(validate_input(addMessage))
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/application")
        
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
        user = User.query.filter_by(id=userID).first()

        if not user:
            flash("Sorry, an error occured! Please re-login", "danger")
            return redirect("/login")
        
        regNum = user.registrationNumber
        existing_application = Application.query.filter_by(registrationNumber=regNum).first()
        if existing_application:
            flash("You have already submitted an application.", "warning")
            return redirect("/")
        
        user.lastname = lastname
        user.phone = phone
        user.dob = dob
        user.program = program
        user.intake = intake
        user.edubackground = edubackground
        user.addMessage = addMessage

        try:
            db.session.commit()
        except Exception as e:
            flash(f"An error occured: {str(e)}", "danger")
            return redirect("/application")
        
        send_applicationConfirmation(email, firstname)
        flash("Your application is successful! Please check your email or student dashboard for more information.", "success")
        return redirect("/application")  
          
    return render_template("application.html")

