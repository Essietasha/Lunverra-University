from flask_mail import Message
from app import mail
from flask import current_app


def send_studentID(email, firstname, registrationNumber):

    userFirstname = firstname[:1].upper() + firstname[1:]

    idMessge = Message(f'Welcome to Lunverra University, {userFirstname}! 🎓',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email] )
    idMessge.body = f"""
Hi {userFirstname}!👋

You have successfully signed up at Lunverra University. 

🆔 Your Registration Number is {registrationNumber}
🔐 Your Password remains the same.

You can now Login to the website using this Registration Number and your PASSWORD!

Warm regards,  
Lunverra Team 🌟
"""
    mail.send(idMessge)


def send_applicationConfirmation(email, firstname):

    userFirstname = firstname[:1].upper() + firstname[1:]

    applicationMessge = Message('Your application at Lunverra is successful!',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email] )
    applicationMessge.body = f"""
Hi {userFirstname}!
You have successfully applied to Lunverra University. 🎓

Your application is now under review. Please be prepared for a virtual interview, 
which is usually scheduled two weeks after your application. Prepare all your documents 
ahead and keep an eye on your email inbox (and spam folder) for the interview 
invitation and other important updates.

If you have any questions, feel free to contact our admissions office at 
admissions@lunverra.edu.

Kindly check your mails at intervals for further notifications!

Warm regards,  
Lunverra Team 🌟 
"""
    mail.send(applicationMessge)


def send_approvalConfirmation(email, firstname, program):

    userFirstname = firstname[:1].upper() + firstname[1:]

    applicationMessge = Message('Your application Has Been Approved!',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email] )
    applicationMessge.body = f"""
Dear {userFirstname},

Congratulations!
We are pleased to inform you that your application to study {program} at Lunverra University has been approved
and you have been admitted into our university. 🎓

You may now proceed to register your courses on the school's website.
Thank you for choosing us. We look forward to welcoming you.

If you have any questions, feel free to contact our admissions office at 
admissions@lunverra.edu.


Best regards,  
The Admissions Team 🌟 
"""
    mail.send(applicationMessge)



