"""Tables for desai Sleep Launch Page and connection to database"""
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, String, LargeBinary


db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///SleepConsultants', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class Referral(db.Model):
    """Referrals stored in db."""
    __tablename__ = "referrals"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,)
    referring = db.Column(db.String,)
    clinic = db.Column(db.String,)
    specialty = db.Column(db.String,)
    referring_contact = db.Column(db.String,)
    reason = db.Column(db.String,)
    fname = db.Column(db.String,)
    lname = db.Column(db.String,)
    phone = db.Column(db.String,)
    additional = db.Column(db.String,)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow,)

    def __repr__(self):
        """show info about the referral"""

        return f"<Referral ID={self.id} Referring Provider={self.referring}, Specialty = {self.specialty}, Referral Contact Info = {self.referring_contact}, Reason for Referral = {self.reason}, Patient First Name = {self.fname}, Patient Last Name = {self.lname}, Patient Phone = {self.phone}, Additional Information = {self.additional} >"


class Call_Request(db.Model):
    """Patient Requesting a Call"""

    __tablename__ = "call"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    fname = db.Column(db.String,)
    lname = db.Column(db.String,)
    phone = db.Column(db.Integer,)
    email = db.Column(db.String,)
    time_selection = db.Column(db.Integer,)
    day_of_week = db.Column(db.String,)
    subject = db.Column(db.String,)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow,)

    def __repr__(self):
        """show info about the call request"""

        return f"<Request ID = {self.id}, First Name ={self.fname}, Last Name={self.lname}, Phone = {self.phone}, Email = {self.email}, Time to Call = {self.time_selection}, Subject = {self.subject}.>"


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
#  68
# SleepConsultants/model.py
# @@ -0,0 +1,68 @@
