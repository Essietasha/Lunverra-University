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
Responsive design.

### Overview
<p align="center">
  <img src="https://github.com/user-attachments/assets/17e89ac1-2056-49d1-9347-54cb2788e6ad" width="80%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/00f434bf-4ab2-4dc9-a69a-e5c78cf4c2bc" width="80%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/6d43e618-0a19-45db-a46e-8262ddb23a90" width="80%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/0926376a-e0c5-48bc-aee0-30d418ce2bd0" width="80%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/c240f82a-2093-4377-a99f-51f46655320a" width="80%">
</p>

## Tech Stack
### Backend
Python, Flask, Flask-SQLAlchemy, Flask-Session, Flask-Migrate

### Frontend
HTML, Sass/SCSS, Jinja2
	
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
