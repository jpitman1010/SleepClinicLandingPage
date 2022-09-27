"""Server for Sleep Consultants Landing Page."""
from flask import Flask, render_template, request, flash, session, redirect, url_for
# from model import connect_to_db, db, CallRequest, Referral
# import crud
import os
import sys
from jinja2 import StrictUndefined
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """View Homepage"""
    return render_template('index.html')


@app.route('/refer_patient', methods=['POST'])
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

    refer_patient = crud.refer_patient(
        referring, clinic, specialty, referring_contact, reason, fname, lname, phone, additional)

    session['referring'] = referring
    session['clinic'] = clinic
    session['specialty'] = specialty
    session['referring_contact'] = referring_contact
    session['reason'] = reason
    session['fname'] = fname
    session['lname'] = lname
    session['phone'] = phone
    session['additional'] = additional

    return redirect(url_for('/referral_successful'))


@ app.route('/referral_success')
def referral_successful():
    """Show Referral Successful html page"""
    referring = sessions['referring']
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

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()
    password = os.environ['password']
    my_email = os.environ['email']

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(my_email, password)

    sender_email = my_email
    receiver_email = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", port)
        server.ehlo()  # Can be omitted
        server.starttls(context=None)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)

    except Exception as e:
        # Print any error messages to stdout
        print(e)

    message = MIMEMultipart("alternative")
    message["Subject"] = f"SECURE: Phone Call Request: {day_of_week} at {time_selection} "
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Cc"] = sender_email

    # Create the plain-text and HTML version of your message
    text = f"""
    A request for a phone call has been placed:

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
    A request for a phone call has been placed:

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

    # Create secure connection with server and send email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    return redirect(url_for('successful_call_request'))


@ app.route('/successful_call')
def successful_call_request():
    """render template for successful call request"""
    return render_template('call_request_success.html')


if __name__ == '__main__':

    # connect_to_db(app)

    app.run(host='0.0.0.0', debug=True, use_reloader=True)
