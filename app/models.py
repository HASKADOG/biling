from app import db
from datetime import datetime

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(64), index=True, unique=True)
    is_arch = db.Column(db.String(120), index=True)
    date = db.Column(db.Integer)
    paid = db.Column(db.String(2), index=True)

    def __init__(self, number, is_arch, date, paid):
        self.number = number
        self.is_arch = is_arch
        self.date = date
        self.paid = paid


    def __repr__(self):
        return '<Contract {} {} {} {} {}>'.format(self.id, self.number, self.is_arch, self.date, self.paid)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(64), index=True, unique=True)
    date = db.Column(db.Integer)

    def __repr__(self):
        return '<Contracth {} {} {}>'.format(self.username)