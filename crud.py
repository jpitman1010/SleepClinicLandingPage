"""Server operations. CRUD = create,read,update,delete"""

from model import Call_Request, Referral, db
from flask import flash, redirect, render_template
import smtplib
import ssl


def refer_patient(referring, clinic, specialty, referring_contact, reason, fname, lname, phone, additional):
    """Create and return a new user."""

    referral = Referral(referring=referring.title(), clinic=clinic.title(), specialty=specialty.title(
    ), referring_contact=referring_contact, reason=reason, fname=fname.title(), lname=lname.title(), phone=phone, additional=additional)

    db.session.add(referral)
    db.session.commit()

    return referral


def request_call(fname, lname, phone, email, time_selection, day_of_week, subject):
    """Create and call request for scheduling team."""

    call_request = Call_Request(fname=fname.title(
    ), lname=lname.title(), phone=phone, email=email, time_selection=time_selection, day_of_week=day_of_week, subject=subject)

    db.session.add(call_request)
    db.session.commit()

    return call_request


port = 465  # For SSL
password = input("Type your password and press enter: ")

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("jpitman1010@gmail.com", password)
    # TODOlist: Send email here
    return render_template('call_request_success.html')


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
