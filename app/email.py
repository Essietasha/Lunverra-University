from flask_mail import Message
from app import mail
from flask import current_app


def send_studentID(email, firstname, registrationNumber):

    idMessge = Message('You have successfully signed up at Lunverra University!',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email] )
    idMessge.body = f"""
Hi {firstname}!

You have successfully signed up at Lunverra University. 

Your Registration Number is {registrationNumber}:
Your Password remains the same.

Kindly Login using your STUDENT ID and your PASSWORD!

Warm regards,  
Lunverra
"""
    mail.send(idMessge)


def send_applicationConfirmation(email, firstname):

    applicationMessge = Message('Your application is successful!',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email] )
    applicationMessge.body = f"""
Hi {firstname}!
You have successfully applied to Lunverra University. 

Your application is now under review. Please be prepared for a virtual interview, 
which is usually scheduled two weeks after your application. Prepare all your documents 
ahead and keep an eye on your email inbox (and spam folder) for the interview 
invitation and other important updates.

If you have any questions, feel free to contact our admissions office at 
admissions@lunverra.edu.

Kindly check your mails at intervals for further notifications!

Warm regards,  
Lunverra.
"""
    mail.send(applicationMessge)



