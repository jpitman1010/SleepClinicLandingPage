import os
import win32com.client as win32
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, session, redirect, url_for
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from PyPDF2 import PdfWriter, PdfReader


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
UPLOAD_FOLDER = "./static/upload"
app.config[UPLOAD_FOLDER] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png', 'jpeg', 'png'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def email(subject, to_email, message, file=None):
    """sending email"""

    # constructing Outlook application instance
    outlook_app = win32.Dispatch('Outlook.Application')
    outlook_object = outlook_app.GetNameSpace('MAPI')


    print(message)
    # constructing the email item object
    mail_item = outlook_app.CreateItem(0)

    mail_item.Subject = subject
    mail_item.BodyFormat = 1
    mail_item.Body = message
    mail_item.To = to_email
    # mail_item.From = 'j.pitman@nioa.gr'

    if file != None:
        if allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))

            #replace with destination location on hosting site
            mail_item.Attachments.Add(r'C:\Users\jpitman\Desktop\SleepClinicLandingPage\static\upload' + '/' + file.filename)
            print('app.request_class type ==',type(app.request_class))
            inputStream = open(r'C:\Users\jpitman\Desktop\SleepClinicLandingPage\static\upload' + '/' + file.filename, 'rb')
            blankStream = open(r'C:\Users\jpitman\Desktop\SleepClinicLandingPage\static\upload\blank.pdf', 'rb')
            output = PdfWriter()
            input = PdfReader(inputStream)
            blank = PdfReader(blankStream)
            del input
            inputStream.close()
            del blank
            blankStream.close()
            outputStream = open(r'C:\Users\jpitman\Desktop\SleepClinicLandingPage\static\upload' + '/' + file.filename, 'wb')
            output.write(outputStream)
            outputStream.close()
            os.remove(r'C:\Users\jpitman\Desktop\SleepClinicLandingPage\static\upload' + '/' + file.filename)
        else:
            flash("Sorry this file-type is not allowed. Please upload only PDF, jpg, jpeg, tiff or png file types.")        


    #for deployment comment out Display() and uncomment Send()
    mail_item.Display()
    # mail_item.Send()
    return


def call_request_message_to_schedulers(fname, lname, date_of_birth, phone, pt_email, time_selection, day_of_week,additional_info, insurance, policy):
    """creating the call request email to send to the schedulers"""

    subject = f"SECURE: Phone Call Request: {day_of_week} at {time_selection}"
    to_email = "email_to_schedulers@outlook.com"


    # Create the plain-text and HTML version of  message
    message = f"""
    A request for a phone call has been placed:

    First Name: {fname}
    Last Name: {lname}
    DOB: {date_of_birth}
    Phone Number: {phone}
    Email: {pt_email}
    Time Patient is Available to take Call: {time_selection} - Day: {day_of_week}
    Subject: {additional_info}
    Insurance: {insurance}
    Policy ID: {policy}


    """
    #if html format for email is wanted: 
    # message = f"""
    # <html>
    # <body>
    #     <p>
    # A request for a phone call has been placed:<br>

    # <b>First Name:</b> {fname}<br>
    # <b>Last Name:</b> {lname} <br>
    # <b>Phone Number:</b> {phone} <br>
    # <b>Email:</b> {email} <br>
    # <b>Time Patient is Available to take Call:</b> {time_selection}<br>
    # <b>Day of Week to Call Patient:</b> {day_of_week}<br>
    # <b>Subject:</b> {additional_info}<br>
    #     </p>
    # </body>
    # </html>
    # """

    email(subject, to_email, message)
    return 


def call_request_message_to_patient(fname, pt_email, time_selection, day_of_week):
    """creating the call request email to send paperwork links to patient to fill out and confirmation of request"""

    subject = f"Sleep Medicine Consultants Appointment Request Confirmation"
    to_email = pt_email
   
    message = f"""

    Your request for a phone call has been placed:

    {fname},
    Your request for scheduling an appointment has been submitted to our scheduling team.  We will do our best to call you on a {day_of_week} between {time_selection}.
    With the insurance information you provided, we are verifying your insurance and the associated costs so that we have this information when we contact you to schedule the appointment.
    This process usually takes 2-5 business days, you will hear from us once this is complete.
    
    In the meantime, please fill out the following intake forms to expedite the process for intake:

    https://hushforms.com/sleepdoc-9962
    https://hushforms.com/sleepdoc-3403
    https://hushforms.com/sleepdoc-9292
    https://www.sleepdoc.net/_files/ugd/657de1_66294ef1daa844719ba2bf42f979441a.pdf
    https://hushforms.com/formcovid2020
    https://secure.hushmail.com/mail/?secureform=financial&subject=Sleep%20Medicine%20Consultants%3A%20Financial%20Form#compose
   
    We look forward to helping improve your sleep!  
    
    Sincerely,
    
    
    Sleep Medicine Consultants
    """
    email(subject, to_email, message)
    return 


def referral_message_to_schedulers(fname, lname, phone, reason, referring, clinic, specialty, referring_contact, file, additional=None):
    """creating the referral email to send to the schedulers"""

    subject = f"SECURE: Referral: From {referring} at {clinic}"
    to_email = "email_to_schedulers@outlook.com"
    message = message = f"""
    A referral has been placed:

    Patient Information:
    First Name: {fname}
    Last Name: {lname}
    Phone Number: {phone}
    Reason for referral: {reason}
    Additional Information (if included): {additional}


    Referral Source Information:
    Referral is from: {referring}
    Clinic referral is from: {clinic}
    Specialty of referring provider: {specialty}
    Referral contact info: {referring_contact}

    """

     
    email(subject, to_email, message, file)
    return 


@app.route('/')
def show_homepage():
    """View Homepage"""
    return render_template('index.html')



@ app.route('/call_request', methods=["POST"])
def call_requested():
    """Handling the  request for a call."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    date_of_birth = request.form.get('dob')
    pt_email = request.form.get('email')
    phone = request.form.get('phone')
    time_selection = request.form.get('timeSelection')
    day_of_week = request.form.get('dayOfWeek')
    additional_info = request.form.get('subject')
    policy = request.form.get('policy_id')
    insurance = request.form.get('insurance')

    call_request_message_to_schedulers(fname, lname, date_of_birth, pt_email, phone, time_selection, day_of_week, additional_info, insurance, policy)
    call_request_message_to_patient(fname, pt_email, time_selection, day_of_week)

    return redirect(url_for('successful_call_request'))


@ app.route('/successful_call')
def successful_call_request():
    """render template for successful call request"""
    return render_template('call_request_success.html')



@app.route('/refer_patient', methods=['GET', 'POST'])
def referral():
    """take user registration info and make cookies"""
    referring = request.form.get('referring')
    clinic = request.form.get('clinic')
    specialty = request.form.get('specialty')
    referring_contact = request.form.get('referring_contact')
    reason = request.form.get('reason')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone = request.form.get('phone')
    additional = request.form.get('additional')
    file = request.files.get('file')

    session['referring'] = referring
    session['clinic'] = clinic
    session['specialty'] = specialty
    session['referring_contact'] = referring_contact

    
    referral_message_to_schedulers(fname, lname, phone, reason, referring, clinic, specialty, referring_contact, file, additional)
   
    return redirect(url_for('referral_successful'))

@ app.route('/referral_success')
def referral_successful():
    """Show Referral Successful html page"""
    return render_template('referral_success.html')



if __name__ == '__main__':

    app.run(host='localhost', debug=True, use_reloader=True, port=5000)

    # app.run(host='0.0.0.0', debug=True, use_reloader=True)
