import os
import win32com.client as win32
# on windows  pip3 install pywin32
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, session, redirect, url_for
from email.mime.multipart import MIMEMultipart


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

    message = MIMEMultipart()
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

    to_email = 'j.pitman@nioa.gr'
    send_email = 'j.pitman@nioa.gr'

    # constructing Outlook application instance
    outlook_app = win32.Dispatch('Outlook.Application')
    outlook_object = outlook_app.GetNameSpace('MAPI')

    # constructing the email item object
    mail_item = outlook_app.CreateItem(0)

    mail_item.Subject = f"SECURE: Referral: From {referring} at {clinic}"
    mail_item.BodyFormat = 1
    mail_item.Body = message
    mail_item.To = to_email

    for file in files:
        mail_item.Attachments.Add(os.path.join(os.getcwd(file), file.filename))

    mail_item.Send()

    return redirect(url_for('referral_successful'))
