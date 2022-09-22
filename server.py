"""Server for Sleep Consultants Landing Page."""
from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db, Call_Request, Referral
import crud
import os
import sys
from jinja2 import StrictUndefined
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    return render_template('/referral_success.html', referring=referring)


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
    # port = 1025
    # for local host
    password = input("Type your password and press enter: ")

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("my@gmail.com", password)
    # TODO: Send email here

    sender_email = "jpitman1010@gmail.com"
    receiver_email = email
    password = input("Type your password and press enter:")
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

    message = MIMEMultipart("alternative")
    message["Subject"] = "SECURE: Phone Call Request: {{session['time_selection']}} "
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Cc"] = sender_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    A request for a phone call has been placed:  
    
    First Name: {{session['fname']}} 
    Last Name: {{session['lname']}} 
    Phone Number: {{session['phone']}} 
    Email: {{session['email']}} 
    Time Patient is Available to take Call: {{session['time_selection']}} - Day: {{session['day_of_week']}} 
    Subject: {{session['subject']}} 

    
    """
    html = """\
    <html>
    <body>
        <p>
    A request for a phone call has been placed:  
    
    <b>First Name:</b> {{session['fname']}} <br>
    <b>Last Name:</b> {{session['lname']}} <br>
    <b>Phone Number:</b> {{session['phone']}} <br>
    <b>Email:</b> {{session['email']}} <br>
    <b>Time Patient is Available to take Call:</b> {{session['time_selection']}} <br>
    <b>Day of Week to Call Patient:</b> {{session['day_of_week]}}<br>
    <b>Subject:</b> {{session['subject']}} <br>
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

    request_call = crud.request_call(
        fname, lname, phone, email, time_selection, day_of_week, subject)
    return render_template('/call_request_success.html', request_call=request_call, fname=fname)


if __name__ == '__main__':

    connect_to_db(app)

    app.run(host='0.0.0.0', debug=True, use_reloader=True)
