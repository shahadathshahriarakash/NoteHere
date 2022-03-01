from . import db
from flask_login import UserMixin
from sqlalchemy import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))
    notes = db.relationship('Note')