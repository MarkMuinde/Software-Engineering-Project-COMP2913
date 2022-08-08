from flask_wtf import Form
from wtforms.fields.html5 import DateField
from wtforms import StringField, IntegerField, TextField, DateField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Customer, Employee, Admin

#Class with details of Judas and the Black Messiah movie
class BookingJudas(Form):
    name = 'Judas and the Black Messiah'
    cast = 'Daniel Kaluuya, Lakeith Stanfield, Jesse Plemons, Dominique Fishback, Ashton Sanders, Darell Britt-Gibson'
    genre = 'Drama/Historical drama'
    director = 'Shaka King'
    production = '2021'
    runtime = '2h 6m'
    ageRestrictions = 'R'

    srcImg= "/static/img/blkjudas.png"

#Class with details of Mortal Kombat movie
class BookingMK(Form):
    name = 'Mortal Kombat'
    cast = 'Josh Lawson, Jessica McNamee, Hiroyuki Sanada'
    genre = 'Fantasy/Action'
    director = 'Simon McQuoid'
    production = '2021'
    runtime = '1h 45m'
    ageRestrictions = 'R'

    srcImg= "/static/img/mk.png"
    

#Class with details of Coming 2 America movie
class BookingComing2(Form):
    name = 'Coming 2 America'
    cast = 'Eddie Murphy, Arsenio Hall, Jermaine Fowler, Leslie Jones, Teyana Taylor, Wesley Snipes'
    genre = 'Comedy/Rom-Com'
    director = 'Craig Brewer'
    production = '2021'
    runtime = '2h'
    ageRestrictions = 'R'

    srcImg= "/static/img/coming2america.png"


#Class with details of Spiderman 3 movie
class BookingSpiderman(Form):
    name = 'Spiderman 3'
    cast = 'Tom Holland, Zendaya, Jacob Batalon, Jamie Foxx, Marisa Tomei'
    genre = 'Adventure/Action/Sci-Fi'
    director = 'Jon Watts'
    production = '2021'
    runtime = '1h 40m'
    ageRestrictions = 'PG-13'

    srcImg= "/static/img/spiderman3.png"

#Class with details of The Forever Purge movie
class BookingPurge(Form):
    name = 'The Forever Purge'
    cast = 'Ana de la Reguera, Josh Lucas, Tenoch Huerta, Leven Rambin'
    genre = 'Action/Horror/Sci-Fi'
    director = 'Everado Gout'
    production = '2021'
    runtime = '1h 15m'
    ageRestrictions = 'R'

    srcImg= "/static/img/foreverpurge.png"

#Class with details of Venom movie
class BookingVenom(Form):
    name = 'Venom: Let There Be Carnage'
    cast = 'Tom Hardy, Woody Harrelson, Michelle Williams, Reid Scott, Naomie Harris'
    genre = 'Action/Horror/Sci-Fi'
    director = 'Andy Serkis'
    production = '2021'
    runtime = '2h'
    ageRestrictions = 'PG-13'

    srcImg= "/static/img/venom.png"

#Class for customer Login
class customerRegistration(Form):
    usernameCustomer = StringField('Username', validators=[DataRequired()])
    dateOfBirth = DateField('Date', format='%Y-%m-%d',
                            validators=[DataRequired(message='Please enter a valid date of the format YYYY-MM-DD')])
    emailCustomer = TextField('Email', validators=[DataRequired(), Email()])
    passwordCustomer = PasswordField('Password', validators=[DataRequired()])
    passwordCustomerVerify = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('passwordCustomer', message='Both passwords must match')])

    def validate_usernameCustomer(self, usernameCustomer):
        usernameCustomer = Customer.query.filter_by(
            usernameCustomer=usernameCustomer.data).first()
        if usernameCustomer:
            raise ValidationError("Username already in use. Please use a different username.")

    def validate_emailCustomer(self, emailCustomer):
        emailCustomer = Customer.query.filter_by(emailCustomer=emailCustomer.data).first()
        if emailCustomer:
            raise ValidationError("Email already in use. Please use a different email address.")

class employeeRegistration(Form):
    employeeName = StringField('Name', validators=[DataRequired()])
    emailEmployee = TextField('Email', validators=[DataRequired(), Email()])
    passwordEmployee = PasswordField('Password', validators=[DataRequired()])
    passwordEmployeeVerify = PasswordField('Repeat password', validators=[
                                           DataRequired(), EqualTo('passwordEmployee', message='Both passwords must match')])

    def validate_emailEmployee(self, emailEmployee):
        emailEmployee = Employee.query.filter_by(emailEmployee=emailEmployee.data).first()
        if emailEmployee:
            raise ValidationError(
                "Email already in use. Please use a different email address.")

class adminRegistration(Form):
    adminName = StringField('Name', validators=[DataRequired()])
    emailAdmin = TextField('Email', validators=[DataRequired(), Email()])
    passwordAdmin = PasswordField('Password', validators=[DataRequired()])
    passwordAdminVerify = PasswordField('Repeat password', validators=[
                                        DataRequired(), EqualTo('passwordAdmin', message='Both passwords must match')])

    def validate_emailAdmin(self, emailAdmin):
        emailAdmin = Admin.query.filter_by(emailAdmin=emailAdmin.data).first()
        if emailAdmin:
            raise ValidationError(
                "Email already in use. Please use a different email address.")

class customerLogin(Form):
    emailCustomer = TextField('email', validators=[DataRequired()])
    passwordCustomer = PasswordField('password', validators=[DataRequired()])

class employeeLogin(Form):
    emailEmployee = TextField('email', validators=[DataRequired()])
    passwordEmployee = PasswordField('password', validators=[DataRequired()])

class adminLogin(Form):
    emailAdmin = TextField('email', validators=[DataRequired()])
    passwordAdmin = PasswordField('password', validators=[DataRequired()])
