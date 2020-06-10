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


class Deals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    name = db.Column(db.String(64))
    type = db.Column(db.Integer)
    old_paid = db.Column(db.Integer)
    old_date = db.Column(db.Integer)
    revert = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)

    def __init__(self, num, name, type, old_paid, old_date, revert, deleted):
        self.name = name
        self.num = num
        self.type = type
        self.old_paid = old_paid
        self.old_date = old_date
        self.revert = revert
        self.deleted = deleted

    def __repr__(self):
        return '<Deal {} {} {} {} {} {} {} {}'.format(self.id, self.num, self.name, self.type, self.old_paid,
                                                      self.old_date, self.revert, self.deleted)
