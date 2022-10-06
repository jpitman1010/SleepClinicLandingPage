"""Server for Sleep Consultants Landing Page."""
import os
from os.path import basename
from pdf_mail import sendpdf
# import sys
import json
from pathlib import Path
import ssl
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
import imghdr
from email.message import EmailMessage
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.utils import secure_filename
import static.upload


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
upload = './static/upload'
app.config['uploadFolder'] = upload


def send_email(message):
    """sending email"""

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    my_email = 'an_email_address'
    password = 'a password'

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(my_email, password)

    sender_email = 'jpitman1010@gmail.com'

    try:
        server = smtplib.SMTP("smtp.gmail.com", port)
        server.ehlo()  # Can be omitted
        server.starttls(context=None)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)

    except Exception as e:
        # Print any error messages to stdout
        print(e)

    # Create secure connection with server and send email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, sender_email, message
        )

    return


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
    files = request.files.getlist('files')
    print('files = ', files)
    print('type(files)', type(files))

    session['referring'] = referring
    session['clinic'] = clinic
    session['specialty'] = specialty
    session['referring_contact'] = referring_contact

    sender_email = 'jpitman1010@gmail.com'
    password = 'jidnywydmewkxzuj'

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = sender_email
    subject = f"SECURE: Referral: From {referring} at {clinic}"
    message["Subject"] = f"SECURE: Referral: From {referring} at {clinic}"
    Create the plain-text and HTML version of your message
    text = f"""
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
    html = f"""
    <html>
    <body>
        <p>
    A referral has been placed:<br><br>

    <b>Patient Information</b>
    <b>First Name:</b> {fname}<br>
    <b>Last Name:</b> {lname} <br>
    <b>Phone Number:</b> {phone} <br>
    <b>Reason for Referral:</b> {reason} <br>
    <b>Additional Information (if included)</b> {additional}<br>

    <b>Referral Source Information</b>
    <b>Referral is from :</b> {referring}<br>
    <b>Clinic referral is from :</b> {clinic}<br>
    <b>Specialty of referring provider :</b> {specialty}<br>
    <b>Referral contact info:</b> {referring_contact}<br>

        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    to_send.email_send()
    for file in files:
        # file.save(os.path.join(app.config['uploadFolder'], file.filename))
        print('this is the file in the for loop =', file.filename)

        with open(upload + "/" + file.filename, 'rb') as f:
            attachment = MIMEApplication(
                f.read(), Name=basename(file.filename))
            attachment['Content-Disposition'] = 'attachment; file="{}"'.format(
                basename(file.filename))
            encoders.encode_base64(attachment)
            message.attach(attachment)
            f.close()
    send_email(message)

    return redirect(url_for('referral_successful'))


@ app.route('/referral_success')
def referral_successful():
    """Show Referral Successful html page"""
    return render_template('referral_success.html')


@ app.route('/call_request', methods=["POST"])
def call_requested():
    """Handling the  request for a call."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    time_selection = request.form.get('timeSelection')
    day_of_week = request.form.get('dayOfWeek')
    subject = request.form.get('subject')

    sender_email = 'sender_email@gmail.com'

    message = MIMEMultipart("alternative")
    message["Subject"] = f"SECURE: Phone Call Request: {day_of_week} at {time_selection}"
    message["From"] = sender_email
    message["To"] = sender_email
    message["Cc"] = email

    # Create the plain-text and HTML version of your message
    text = f"""
    A request for a phone call has been placed:<br>

    First Name: {fname}
    Last Name: {lname}
    Phone Number: {phone}
    Email: {email}
    Time Patient is Available to take Call: {time_selection} - Day: {day_of_week}
    Subject: {subject}

    """
    html = f"""
    <html>
    <body>
        <p>
    A request for a phone call has been placed:<br>

    <b>First Name:</b> {fname}<br>
    <b>Last Name:</b> {lname} <br>
    <b>Phone Number:</b> {phone} <br>
    <b>Email:</b> {email} <br>
    <b>Time Patient is Available to take Call:</b> {time_selection}<br>
    <b>Day of Week to Call Patient:</b> {day_of_week}<br>
    <b>Subject:</b> {subject}<br>
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    send_email(message)

    return redirect(url_for('successful_call_request'))


@ app.route('/successful_call')
def successful_call_request():
    """render template for successful call request"""
    return render_template('call_request_success.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True, use_reloader=True)
