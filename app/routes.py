from flask import render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
import re, bleach, random
from app.helpers import login_required
from datetime import datetime, timezone
from app.models import User, Application
from app.email import send_studentID, send_applicationConfirmation, send_approvalConfirmation

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

@app.context_processor
def userStatus():
    user = None
    is_admin = False

    if "userID" in session:
        user = User.query.get(session["userID"])
        is_admin = user.is_admin if user else False

    return {
        "authenticated": user is not None,
        "is_admin": is_admin,
        "current_user": user
    }


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
        firstname = request.form.get("firstname").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        if not firstname or not email or not password or not confirmpassword:
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
            flash("Password must be at least 8 characters!", "danger")
            return redirect("/signup")

        try:
            firstname = sanitize_input(validate_input(firstname)).lower()
            email = sanitize_input(validate_input(email))
            validate_password(password)
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/signup")
        
        existingUser = User.query.filter_by(email=email).first()
        if existingUser:
            flash(f"An account with {email} already exists. Try loging in.", "danger")
            return redirect("/signup")
        
        password= generate_password_hash(password)
        registeredNumber = "LUNV2025" + firstname[:2] + firstname[-1] + str(random.randint(10000, 99999))

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
            regNum = sanitize_input(validate_input(regNum))
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/login")
        
        user = User.query.filter_by(registrationNumber=regNum).first()

        if not user or not check_password_hash(user.hashedPassword, password):
            flash("Registration Number or Password incorrect!", "danger")
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
    user = User.query.filter_by(id=userID).first()
    firstname = user.firstname[:1].upper() + user.firstname[1:]

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
            if addMessage:
                addMessage = sanitize_input(validate_input(addMessage))
            else:
                addMessage = None
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
            flash("You have already submitted an application. Visit your dashboard to review.", "warning")
            return redirect("/")

        new_Application = Application(registrationNumber=regNum)
        db.session.add(new_Application)
        
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
        flash("Your application is successful! Please check your email or dashboard for more information.", "success")
        return redirect("/dashboard")  
          
    return render_template("application.html", firstname=firstname, email=user.email)


@app.route("/approveapplications", methods=["GET", "POST"])
@login_required
def approve_applications():

    applications = db.session.query(Application, User).join(
        User, Application.registrationNumber == User.registrationNumber
    ).all()
    
    if request.method == "POST":
        regNum = request.form.get("registrationNumber")

        if not regNum:
            flash("Registration number is missing.", "danger")
            return redirect("/approveapplications")

        user = User.query.filter_by(registrationNumber=regNum).first()

        if user:
            user.is_approved = True
            email = user.email
            firstname = user.firstname
            program = user.program

            db.session.commit()
            send_approvalConfirmation(email, firstname, program)
            flash(f"{user.firstname}'s application is now approved!", "success")
        else:
            flash("User not found.", "danger")
        return redirect("/approveapplications")

    return render_template("approveapplications.html", applications=applications)


@app.route("/dashboard")
@login_required
def dashboard():
    userID = session.get("userID")

    userProfile = User.query.filter_by(id=userID).first()
    if not userProfile:
        flash("User not found.", "danger")
        return redirect("/login")

    userRegNum = userProfile.registrationNumber
    userfirstname = userProfile.firstname[:1].upper() + userProfile.firstname[1:]

    appDate = Application.query.filter_by(registrationNumber=userRegNum).first()
    app_date = appDate.application_date if appDate else None

    return render_template("dashboard.html", userProfile=userProfile, app_date=app_date, userfirstname=userfirstname)


@app.route("/students")
@login_required
def students():

    userID = session.get("userID")
    admin = User.query.filter_by(id=userID).first()

    if not admin or not admin.is_admin:
        flash("Access denied. Admins only.", "danger")

    students = User.query.all()
    return render_template("students.html", students=students, isAdmin=admin.is_admin, currentUserID=userID)


@app.route("/deletestudent/<int:studentID>", methods=["POST"])
@login_required
def deleteStudent(studentID):
    userID = session.get("userID")
    admin = User.query.filter_by(id=userID).first()

    if not admin or not admin.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect("/students")
    
    student = User.query.get_or_404(studentID)
    studentRegNum = student.registrationNumber

    studentApplication = Application.query.filter_by(registrationNumber=studentRegNum).first()

    if student.id == userID:
        flash("You cannot delete your own account.", "warning")
        return redirect("/students")

    db.session.delete(student)
    if studentApplication:
        db.session.delete(studentApplication)
    db.session.commit()
    flash(f"{student.firstname} has been deleted.", "success")
    return redirect("/students")


@app.route("/courseregistration")
@login_required
def courseregistration():
    userID = session.get("userID")

    return render_template("courseregistration.html")


@app.errorhandler(404)
def pageNotFound(e):
    return render_template("notfound.html", errorMessage=str(e)), 404
