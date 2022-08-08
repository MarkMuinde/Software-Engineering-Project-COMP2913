from app import db,login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json


@login.user_loader
def load_user(id):
    return Customer.query.get(int(id))

    
class Customer(db.Model, UserMixin):   
    id = db.Column(db.Integer,primary_key=True)
    usernameCustomer = db.Column(db.String(50), unique=True, nullable=False)
    dateOfBirth = db.Column(db.DateTime('%Y-%m-%d'), nullable=False)
    emailCustomer = db.Column(db.String(50), unique=True, nullable=False)
    passwordCustomer = db.Column(db.String(200), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def set_password(self, passwordCustomer):
        self.password_hash = generate_password_hash(passwordCustomer)

    def check_password(self, passwordCustomer):
        return check_password_hash(self.password_hash, passwordCustomer)

    def __repr__(self):
        return '{}{}{}{}{}{}'.format(self.id, self.usernameCustomer, self.dateOfBirth, self.emailCustomer, self.passwordCustomer, self.age)


class Employee(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    employeeName = db.Column(db.String(80), unique=False, nullable=False)
    emailEmployee = db.Column(db.String(120), unique=True, nullable=False)
    passwordEmployee = db.Column(db.String(180), unique=False, nullable=False)

    def set_password(self, passwordEmployee):
        self.password_hash = generate_password_hash(passwordEmployee)

    def check_password(self, passwordEmployee):
        return check_password_hash(self.password_hash, passwordEmployee)

    def __repr__(self):
        return '{}{}{}{}'.format(self.id, self.employeeName, self.emailEmployee, self.passwordEmployee)

class Admin(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    adminName = db.Column(db.String(80), unique=False, nullable=False)
    emailAdmin = db.Column(db.String(120), unique=True, nullable=False)
    passwordAdmin = db.Column(db.String(180), unique=False, nullable=False)

    def set_password(self, passwordAdmin):
        self.password_hash = generate_password_hash(passwordAdmin)

    def check_password(self, passwordAdmin):
        return check_password_hash(self.password_hash, passwordAdmin)

    def __repr__(self):
        return '{}{}{}{}'.format(self.id, self.adminName, self.emailAdmin, self.passwordAdmin)


class Movies(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    movieName = db.Column(db.String(50), unique=False, nullable=False)
    isAdultFilm = db.Column(db.Boolean, nullable=False)
    dateOfShow = db.Column(db.DateTime('%Y-%m-%d'))

    def __repr__(self):
        return '{}{}{}{}'.format(self.id, self.movieName, self.isAdultFilm, self.dateOfShow)


class Tickets(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    customerName = db.Column(db.String(50), unique=False, nullable=False)
    movieName = db.Column(db.String(50), unique=False, nullable=False)
    dateOfShow = db.Column(db.Date())
    seatNumber = db.Column(db.String(5), unique=True)
    ticket = db.Column(db.LargeBinary, unique=True)
    bookingDate = db.Column(db.Date())
    numberOfTickets= db.Column(db.Integer)
    revenueGenerated = db.Column(db.Integer)

    def __repr__(self):
        return '{}{}{}{}{}{}{}{}{}'.format(self.id, self.customerName, self.movieName, self.dateOfShow, self.seatNumber, self.ticket, self.bookingDate, self.numberOfTickets, self.revenueGenerated)



db.create_all()
