from flask_login import UserMixin
from application import db
from datetime import datetime
from flask_validator import ValidateString, ValidateInteger, ValidateEmail, ValidateRange


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    # 0 - cashier/teller, 1- customer executives 2-admin
    aadhar = db.Column(db.String(50), nullable=False, unique=True)
    timeStamp = db.Column(db.DateTime, default=datetime.now)

    def is_admin(self):
        if self.type == 2:
            return True

    def is_executive(self):
        if self.type == 1:
            return True

    def is_cashier(self):
        if self.type == 0:
            return True


class customerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssn = db.Column(db.Integer, nullable=False)
    aid = db.Column(db.Integer, nullable=False)
    atpye = db.Column(db.Integer, nullable=False)
    # 0 - saving and 1- current
    status = db.Column(db.String(10), nullable=False)
    msg = db.Column(db.String(500))
    lastUpdated = db.Column(db.DateTime, default=datetime.now)
    balance = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Transaction(db.Model):
    Tid = db.Column(db.Integer, primary_key=True, autoincrement=True)  # its autoincrement
    cid = db.Column(db.Integer, nullable=False)  # consumer ID
    To_account = db.Column(db.Integer)
    type = db.Column(db.String(50))  # type - deposit or withdraw
    dt = db.Column(db.DateTime, default=datetime.now)
    timeStamp = db.Column(db.DateTime, default=datetime.now)
    wamt = db.Column(db.Integer, nullable=False)
    bal = db.Column(db.Integer, nullable=False)


class Customer(db.Model):
    cid = db.Column(db.Integer, primary_key= True, autoincrement = True)
    ssn = db.Column(db.Integer, nullable = False)
    custName = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    addr = db.Column(db.Text, nullable = False)
    stateSelect = db.Column(db.String(20), nullable = False)
    citySelect = db.Column(db.String(20), nullable = False)
    lastUpdated = db.Column(db.DateTime, default = datetime.now)
    atype = db.Column(db.Integer)
    alastUpdated = db.Column(db.DateTime, default = datetime.now)
    balance = db.Column(db.Integer)
