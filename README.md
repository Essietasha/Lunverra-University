# Lunverra University

A university web application built with Python, Flask, and SQLAlchemy that allows students to register, login, and manage courses. Designed as a full-stack university portal.

## Features
Student and Admin Roles
Admins can manage courses and users.
Students can register, login, and enroll in courses.
Course Management
Add, view, and enroll in courses.
Store course details including title, department, and credits.
User Authentication
Email notification 
Secure login with hashed passwords.
Session management using Flask-Session.
Student dashboard 
Database
SQLite for development.
SQLAlchemy ORM for database interactions.
Flask-Migrate for easy schema updates.
Dynamic Frontend
Jinja2 templates with reusable layout for consistent UI.
Responsive HTML/CSS design.



## Tech Stack
### Backend
Python, Flask, Flask-SQLAlchemy, Flask-Session, Flask-Migrate

### Frontend
HTML, CSS, Jinja2
	
### 
Database: SQLite (development)

## Workflow
Registration: Students register with email accounts.
Account Activation: Admin must approve accounts.
Email Verification: Verification email is sent to the registered email address.
Successful Login: Upon email confirmation, students can log in.
Student Dashboard: After login, students can see courses and their profile.
Course Registration: Students can Errol for preferred courses at both departmental and faculty level.
Course Management: Students can add, edit, or remove courses.
Data Handling: Users, courses, and registrations are stored in a database using SQLAlchemy ORM.
