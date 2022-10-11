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
ALLOWED_EXTENSIONS = {'pdf'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def show_homepage():
    """View Homepage"""
    return render_template('index.html')


@app.route('/refer_patient', methods=['GET', 'POST'])
def user_reg_post_intake():
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


    print('files = ', file)
    print('type(attachment)', type(file))

    session['referring'] = referring
    session['clinic'] = clinic
    session['specialty'] = specialty
    session['referring_contact'] = referring_contact

    message = f"""
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

    #if provider prefers HTML format: 
    # html = f"""
    # <html>
    # <body>
    #     <p>
    # A referral has been placed:<br><br>

    # <b>Patient Information</b>
    # <b>First Name:</b> {fname}<br>
    # <b>Last Name:</b> {lname} <br>
    # <b>Phone Number:</b> {phone} <br>
    # <b>Reason for Referral:</b> {reason} <br>
    # <b>Additional Information (if included)</b> {additional}<br>

    # <b>Referral Source Information</b>
    # <b>Referral is from :</b> {referring}<br>
    # <b>Clinic referral is from :</b> {clinic}<br>
    # <b>Specialty of referring provider :</b> {specialty}<br>
    # <b>Referral contact info:</b> {referring_contact}<br>

    #     </p>
    # </body>
    # </html>
    # """

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    # message.attach(part2)

    to_email = 'j.pitman@anEmailAddress.com'
    send_email = 'j.pitman@anEmailAddress.com'

    # constructing Outlook application instance
    outlook_app = win32.Dispatch('Outlook.Application')
    outlook_object = outlook_app.GetNameSpace('MAPI')

    # constructing the email item object
    mail_item = outlook_app.CreateItem(0)

    mail_item.Subject = f"SECURE: Referral: {referring} at {clinic}"
    mail_item.BodyFormat = 1
    print(message)
    mail_item.Body = message
    mail_item.To = to_email

    if file != None:
        if allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))

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
            flash("Sorry this file-type is not allowed.")
    


    #for deployment comment out Display() and uncomment Send()
    mail_item.Display()
    # mail_item.Send()

    return redirect(url_for('referral_successful'))

@ app.route('/referral_success')
def referral_successful():
    """Show Referral Successful html page"""
    return render_template('referral_success.html')



if __name__ == '__main__':

    # app.run(host='localhost', debug=True, use_reloader=True, port=5000)

    app.run(host='0.0.0.0', debug=True, use_reloader=True)
