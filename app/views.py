import logging
from flask import flash, render_template, request, redirect, url_for, jsonify, make_response
from flask_mail import Mail, Message
from flask_login import current_user, login_user, logout_user, login_required
from .models import Customer, Employee, Admin, Movies, Tickets
import config
from .forms import BookingJudas, BookingMK, BookingComing2, BookingSpiderman, BookingVenom, BookingPurge, customerRegistration, employeeRegistration, adminRegistration, customerLogin, employeeLogin, adminLogin
from .user import User
from .transaction import Transaction
import os
from flask_sqlalchemy import inspect
from app import app,db, bcrypt
from werkzeug.urls import url_parse
from time import strftime
from datetime import date
from datetime import timedelta 
from ctypes import cast
import sys
from luhn import *
import pdfkit
from pyvirtualdisplay import Display
import base64
import datetime
from io import BytesIO
import qrcode
from PIL import Image
import pygal


gCurrentUser = User("", 0, False, "")

gCurrentTransaction = Transaction("", "", date(2020, 1, 1),
datetime.time(0,0,0), date(2020, 1, 1), "", 0, 0, 0, 0)

gAllWeekTotal = {}
gAllTicketTotal={}

wkh = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
app.config['DEBUG']=True
#app.config['MAIL_DEBUG']=True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'donotreplygalaxycinema@gmail.com'
app.config['MAIL_PASSWORD'] = 'wonuola01'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['TESTING'] = False
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)

class Movies:
    def __init__(self,title,url,genre,book,dates,adultFilm):
        self.title = title
        self.url = url
        self.genre = genre
        self.book = book
        self.dates = dates
        self.adultFilm = adultFilm

mortal =  Movies("Mortal Kombat","static/img/mk.png","fiction","location.href='bookingsMK'","23/06/2021,24/06/2021,25/06/2021","Yes")     
judas = Movies("Judas And The Black Messiah", "static/img/blkjudas.png", "drama", "location.href='bookingsJudas'", "28/06/2021,29/06/2021,30/06/2021,01/06/2021", "Yes")
coming = Movies("Coming 2 America", "static/img/coming2america.png", "drama","location.href='bookingsComing2'", "01/07/2021,02/07/2021,03/07/2021", "No")
spiderman = Movies("Spiderman 3","static/img/spiderman3.png","fiction","location.href='bookingsSpiderman3'","06/07/2021,07/07/2021,08/07/2021,09/07/2021,10/07/2021", "No")
purge = Movies("The Forever Purge", "static/img/foreverpurge.png", "fiction","location.href='bookingsPurge'", "27/06/2021,28/06/2021,29/06/2021", "Yes")
venom = Movies("Venom: Let There Be Carnage", "static/img/venom.png","fiction", "location.href='bookingsVenom'", "05/07/2021,06/07/2021,07/07/2021", "Yes")

movieList = [mortal,judas,coming,spiderman,purge,venom]

def sendTicketMail():
    
    msg = Message('Ticket Confirmation', sender = 'donotreplygalaxycinema@gmail.com', recipients = [gCurrentTransaction.email])
    msg.body = "You're going to see " + gCurrentTransaction.movie +"!\n\nPlease find your ticket attached and validation QR code attached."
    with app.open_resource("output.pdf") as fp:  
        msg.attach("ticket.pdf", "application/pdf", fp.read())
    with app.open_resource("qrcode.png") as fp:  
        msg.attach("QR.png", "image/png", fp.read())
    mail.send(msg)

def addTicketToDatabase():
    global gCurrentTransaction
    max = 0
    if issubclass(type(gCurrentTransaction.showDate), str):
        gCurrentTransaction.showDate = date.fromisoformat(gCurrentTransaction.showDate)
    if issubclass(type(gCurrentTransaction.bookDate), str):
        gCurrentTransaction.bookDate = date.fromisoformat(gCurrentTransaction.bookDate)

    print(type(gCurrentTransaction.showDate),file=sys.stderr )
    print(type(gCurrentTransaction.bookDate), file=sys.stderr)

    allTickets = Tickets.query.order_by(Tickets.id).all()
    for transaction in allTickets:
        temp = queryToDict(transaction)
        if(temp.get("id") >max):
            max = temp.get("id")
            
    tickets = Tickets(id = max+1,
        customerName = gCurrentTransaction.customerName,
        movieName = gCurrentTransaction.movie,
        dateOfShow =  gCurrentTransaction.showDate,
        seatNumber = "A1,A2",
        ticket = None,
        bookingDate = gCurrentTransaction.bookDate,
        numberOfTickets = gCurrentTransaction.totalNoOfTickets(),
        revenueGenerated = gCurrentTransaction.total)

    db.session.add(tickets)
    db.session.commit()

def queryToDict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def fetchAllWeekIncome(searchDate):
    startDate = datetime.datetime.strptime(searchDate, '%Y-%m-%d')
    endDate = startDate + timedelta(days=7) 

    names = ["Coming 2 America", "Judas And The Black Messiah", "Mortal Kombat","Spiderman 3", "The Forever Purge", "Venom: Let There Be Carnage"]
    for x in names:
        total = 0
        allTickets = Tickets.query.filter(Tickets.bookingDate.between(startDate.date(), endDate.date())).all()

        for transaction in allTickets:
            temp = queryToDict(transaction)
            if(temp.get("movieName") == x):
                total += temp.get("revenueGenerated")
        gAllWeekTotal[x] = total

    print(gAllWeekTotal, file=sys.stderr)

def fetchTickets(date1, date2):
    startDate = date.fromisoformat(date1)
    endDate = date.fromisoformat(date2)

    names = ["Coming 2 America", "Judas And The Black Messiah", "Mortal Kombat","Spiderman 3", "The Forever Purge", "Venom: Let There Be Carnage"]
    for x in names:
        total = 0
        allTickets = Tickets.query.filter(Tickets.bookingDate.between(startDate, endDate)).all()

        for transaction in allTickets:
            temp = queryToDict(transaction)
            if(temp.get("movieName") == x):
                total += temp.get("numberOfTickets")
        gAllTicketTotal[x] = total


# Add pages here

# Homepage
@app.route('/')
def index():
    return render_template("frontPage.html")

@app.route('/order', methods=['GET', 'POST'])
def order():
    app.logger.info('Confirm Page')
    return render_template("order.html")


@app.route('/home')
def home():
    app.logger.info('Homepage Successfully Rendered')
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    return render_template("home.html")

@app.route('/weekGraphs', methods=['GET', 'POST'])
def weekGraphs():
    chart = pygal.Bar()

    if request.method == 'POST':
        date = request.form['date']
        fetchAllWeekIncome(date)
        chart.title = 'Weekly Revenue Generated for week starting ' + date + '(in GBP)'
        total = 0
        for movie in gAllWeekTotal:
            chart.add(movie, [gAllWeekTotal[movie]])
            total += gAllWeekTotal[movie]
        chart.add("Total", [total])

    chart = chart.render_data_uri()
    return render_template('weekGraphs.html', chart = chart)


@app.route('/ticketGraphs', methods=['GET', 'POST'])
def ticketGraphs():
    chart = pygal.Bar()

    if request.method == 'POST':
        date1 = request.form['startDate']
        date2 = request.form['endDate']
        fetchTickets(date1, date2)
        chart.title = 'Tickets sold from ' + date1 + ' to ' + date2
        for movie in gAllTicketTotal:
            chart.add(movie, [gAllTicketTotal[movie]])

    chart = chart.render_data_uri()
    return render_template('ticketGraphs.html', chart = chart)

@app.route('/showtimes')
def displayshowtimes():
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    return render_template("showtimes.html")

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        return

    return render_template("book.html")

#Bookings pages
@app.route('/bookingsMK', methods=['GET', 'POST'])
def bookingMK():
    form = BookingMK()

    if request.method == 'POST':
        global gCurrentTransaction
        gCurrentTransaction.showDate = date.fromisoformat(request.form['date'])
        gCurrentTransaction.setShowTime(request.form['time'])

        today = date.today()
        gCurrentTransaction.bookDate = date.fromisoformat(today.strftime('%Y-%m-%d'))

        gCurrentTransaction.aQuantity = int(request.form['adultQuantity'])
        gCurrentTransaction.sQuantity = int(request.form['seniorQuantity'])
        
        total = gCurrentTransaction.calculateTotal()
        
        if total>0:
            total = format(total, '.2f')
            img = form.srcImg

            gCurrentTransaction.movie = "Mortal Kombat"

            return redirect(url_for("payment", form=form, total=total, img=img))

        
    form = BookingMK()
    return render_template('bookingsMK.html', form=form)

@app.route('/bookingsJudas', methods=['GET', 'POST'])
def bookingJudas():
    form = BookingJudas()

    if request.method == 'POST':
        global gCurrentTransaction
        gCurrentTransaction.showDate = date.fromisoformat(request.form['date'])
        gCurrentTransaction.setShowTime(request.form['time'])

        today = date.today()
        gCurrentTransaction.bookDate = date.fromisoformat(today.strftime('%Y-%m-%d'))

        gCurrentTransaction.aQuantity = int(request.form['adultQuantity'])
        gCurrentTransaction.sQuantity = int(request.form['seniorQuantity'])
        
        total = gCurrentTransaction.calculateTotal()
        
        if total>0:
            total = format(total, '.2f')
            img = form.srcImg

            gCurrentTransaction.movie = "Judas And The Black Messiah"

            return redirect(url_for("payment", form=form, total=total, img=img))

    return render_template('bookingsJudas.html',form=form)

@app.route('/bookingsComing2', methods=['GET', 'POST'])
def bookingComing2():
    form = BookingComing2()
    if request.method == 'POST':
        global gCurrentTransaction
        gCurrentTransaction.showDate = date.fromisoformat(request.form['date'])
        gCurrentTransaction.setShowTime(request.form['time'])

        today = date.today()
        gCurrentTransaction.bookDate = date.fromisoformat(today.strftime('%Y-%m-%d'))

        gCurrentTransaction.aQuantity = int(request.form['adultQuantity'])
        gCurrentTransaction.sQuantity = int(request.form['seniorQuantity'])
        
        total = gCurrentTransaction.calculateTotal()
        
        if total>0:
            total = format(total, '.2f')
            img = form.srcImg

            gCurrentTransaction.movie = "Coming 2 America"

            return redirect(url_for("payment", form=form, total=total, img=img))

    return render_template('bookingsComing2.html',form=form)

@app.route('/bookingsSpiderman3', methods=['GET', 'POST'])
def bookingSpiderman3():
    form = BookingSpiderman()

    if request.method == 'POST':
        global gCurrentTransaction
        print(request.form['date'], file=sys.stderr)
        gCurrentTransaction.showDate = request.form['date']

        today = date.today()
        gCurrentTransaction.bookDate = today.strftime('%Y-%m-%d')
        print(gCurrentTransaction.bookDate, file=sys.stderr)

        gCurrentTransaction.aQuantity = int(request.form['adultQuantity'])
        gCurrentTransaction.cQuantity = int(request.form['childQuantity'])
        gCurrentTransaction.sQuantity = int(request.form['seniorQuantity'])

        
        total = gCurrentTransaction.calculateTotal()
        
        if total>0:
            total = format(total, '.2f')

            img = form.srcImg

            gCurrentTransaction.movie = "Spiderman 3"
            return redirect(url_for("payment", total=total, form=form, img=img))

    form = BookingSpiderman()
    return render_template('bookingsSpiderman3.html',form=form)

@app.route('/bookingsVenom', methods=['GET', 'POST'])
def bookingVenom():
    form = BookingVenom()

    if request.method == 'POST':
        global gCurrentTransaction
        print(request.form['date'], file=sys.stderr)
        gCurrentTransaction.showDate = request.form['date']

        today = date.today()
        gCurrentTransaction.bookDate = today.strftime('%Y-%m-%d')
        print(gCurrentTransaction.bookDate, file=sys.stderr)

        gCurrentTransaction.aQuantity = int(request.form['adultQuantity'])
        gCurrentTransaction.cQuantity = int(request.form['childQuantity'])
        gCurrentTransaction.sQuantity = int(request.form['seniorQuantity'])

        
        total = gCurrentTransaction.calculateTotal()
        
        if total>0:
            total = format(total, '.2f')

            img = form.srcImg

            gCurrentTransaction.movie = "Venom: Let There Be Carnage"
            return redirect(url_for("payment", total=total, form=form, img=img))

    return render_template('bookingsVenom.html',form=form)

@app.route('/bookingsPurge', methods=['GET', 'POST'])
def bookingPurge():
    form = BookingPurge()
    if request.method == 'POST':
        global gCurrentTransaction
        gCurrentTransaction.showDate = date.fromisoformat(request.form['date'])
        gCurrentTransaction.setShowTime(request.form['time'])

        today = date.today()
        gCurrentTransaction.bookDate = date.fromisoformat(today.strftime('%Y-%m-%d'))

        gCurrentTransaction.aQuantity = int(request.form['adultQuantity'])
        gCurrentTransaction.sQuantity = int(request.form['seniorQuantity'])
        
        total = gCurrentTransaction.calculateTotal()
        
        if total>0:
            total = format(total, '.2f')
            img = form.srcImg

            gCurrentTransaction.movie = "The Forever Purge"

            return redirect(url_for("payment", form=form, total=total, img=img))

    return render_template('bookingsPurge.html',form=form)

# Movie Detail Pages
@app.route('/mortalkombat', methods=['GET', 'POST'])
def mortalKombat():
    return render_template("mortalkombat.html")


@app.route('/judas')
def judasMovie():
    return render_template("judas.html")


@app.route('/coming2america')
def coming2America():
    return render_template("coming2america.html")


@app.route('/spiderman3')
def spiderMan3():
    return render_template("spiderman3.html")


@app.route('/purge')
def purge():
    return render_template("purge.html")


@app.route('/venom')
def venom():
    return render_template("venom.html")


# Bookings Page
@app.route('/bookings')
def bookings():
    return render_template("bookings.html")


@app.route('/showtimes')
def showtimes():
    app.logger.info('Showtimes Page Successfully Rendered')
    return render_template("showtimes.html")



def validateCard(cardNum, cardDate, cvv):
    numCheck = False
    dateCheck = False
    cvvCheck = False
    if len(cvv) == 3:
        cvvCheck = True
    
    dateSplit = cardDate.split("/")

    if int(dateSplit[1]) > 21:
        dateCheck = True
    elif int(dateSplit[1]) == 21 and int(dateSplit[0]) > 5:
        dateCheck = True
    
    numCheck = verify(cardNum)
   
    return numCheck and dateCheck and cvvCheck


    

#Bookings pages
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        global gCurrentTransaction
        gCurrentTransaction.customerName = request.form['name']
        gCurrentTransaction.email = request.form['email']  

        if request.form.get("cashPay"):
            tickets = {
                "adult": gCurrentTransaction.aQuantity,
                "child": gCurrentTransaction.cQuantity,
                "senior": gCurrentTransaction.sQuantity
            }

            addTicketToDatabase()
            return redirect(url_for("confirmation", tickets=tickets, name = gCurrentTransaction.movie))
        else:
            gCurrentTransaction.email = request.form['email'] 
            cardNum = request.form['cardNum']  
            cardDate = request.form['cardDate']
            cvv = request.form['cvv']

            if validateCard(cardNum, cardDate, cvv) == True:
                tickets = {
                    "adult": gCurrentTransaction.aQuantity,
                    "child": gCurrentTransaction.cQuantity,
                    "senior": gCurrentTransaction.sQuantity
                }
                
                addTicketToDatabase()

                return redirect(url_for("confirmation", tickets=tickets, name = gCurrentTransaction.movie))
            else:
                flash('Invalid Details')

                return render_template('payment.html',
                    form=request.args.get('form'),
                    total=request.args.get('total'),
                    img=request.args.get('img'))
    else:
        return render_template('payment.html',
            form=request.args.get('form'),
            total=request.args.get('total'),
            img=request.args.get('img')
        )

        

def generateQRCode():
     #Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('Galaxy Cinema Valid Ticket')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save('app\qrcode.png')


@app.route('/confirmation')
def confirmation():
    rendered = render_template("ticket.html",
        movie = gCurrentTransaction.movie,
        name = gCurrentTransaction.customerName,
        date = gCurrentTransaction.showDate,
        time = gCurrentTransaction.showTime,
        num = gCurrentTransaction.totalNoOfTickets(),
        adultQ = gCurrentTransaction.aQuantity,
        childQ = gCurrentTransaction.cQuantity,
        seniorQ = gCurrentTransaction.sQuantity)

    generateQRCode()    
    pdf = pdfkit.from_string(rendered, "app\output.pdf", configuration=wkh)
    sendTicketMail()
    
    return render_template("confirmation.html", 
    tickets=request.args.get('tickets'),
    name=request.args.get('name'))

@app.route('/customerRegistration', methods =['GET', 'POST'])
def CustomerRegistration():
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = customerRegistration()

    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(
            form.passwordCustomer.data)
        now = datetime.datetime.now()
        age = int(now.strftime('%Y')) - int(form.dateOfBirth.data.strftime('%Y'))
        customer = Customer(usernameCustomer=form.usernameCustomer.data,
                            dateOfBirth=form.dateOfBirth.data,
                            emailCustomer=form.emailCustomer.data,
                            passwordCustomer=hash_password,
                            age=age)
        db.session.add(customer)
        db.session.commit()
        flash('Succesfully received form data.')
        app.logger.info('customer successfully added')
        return render_template('home.html')
    return render_template('customerRegistration.html', form=form)


@app.route('/employeeRegistration', methods=['GET', 'POST'])
def EmployeeRegistration():
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = employeeRegistration()

    if form.validate_on_submit():

        hash_password = bcrypt.generate_password_hash(
            form.passwordEmployee.data)
        employee = Employee(employeeName=form.employeeName.data,
                            emailEmployee=form.emailEmployee.data,
                            passwordEmployee=hash_password)
        db.session.add(employee)
        db.session.commit()
        flash('Succesfully received form data.')
        app.logger.info('employee successfully added')
        return render_template('home.html')
    return render_template('employeeRegistration.html', form=form)


@app.route('/adminRegistration', methods=['GET', 'POST'])
def AdminRegistration():
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = adminRegistration()

    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(
            form.passwordAdmin.data)
        admin = Admin(adminName=form.adminName.data,
                      emailAdmin=form.emailAdmin.data,
                      passwordAdmin=hash_password)
        db.session.add(admin)
        db.session.commit()
        flash('Succesfully received form data.')
        app.logger.info('admin successfully added')
        return render_template('home.html')
    return render_template('adminRegistration.html', form=form)

@app.route('/customerLogin', methods =['GET', 'POST'])
def CustomerLogin():       
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = customerLogin()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(
            emailCustomer=form.emailCustomer.data).first()

        if customer is None or not bcrypt.check_password_hash(customer.passwordCustomer, form.passwordCustomer.data):
            flash('Invalid username or password')
            return render_template('customerLogin.html', form=form)

        if customer and bcrypt.check_password_hash(customer.passwordCustomer, form.passwordCustomer.data):
            app.logger.info('customer login  successful')
            flash(f'Welcome {customer.usernameCustomer},{customer.age}')
            currentUserEmail = customer.emailCustomer
            return render_template('home.html')
    return render_template('customerLogin.html', form=form)

@app.route('/employeeLogin', methods =['GET', 'POST'])
def EmployeeLogin():
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = employeeLogin()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(
            emailEmployee=form.emailEmployee.data).first()

        if employee is None or not bcrypt.check_password_hash(employee.passwordEmployee, form.passwordEmployee.data):
            flash('Invalid username or password')
            return render_template('employeeLogin.html', form=form)

        if employee and bcrypt.check_password_hash(employee.passwordEmployee, form.passwordEmployee.data):
            app.logger.info('employee login  successful')
            flash(f'Welcome {employee.employeeName}')
            return render_template('employeeHome.html')
    return render_template('employeeLogin.html', form=form)

@app.route('/adminLogin', methods =['GET', 'POST'])
def AdminLogin():
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = adminLogin()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(emailAdmin=form.emailAdmin.data).first()

        if admin is None or not bcrypt.check_password_hash(admin.passwordAdmin, form.passwordAdmin.data):
            flash('Invalid username or password')
            return render_template('adminLogin.html', form=form)

        gCurrentUser.name = admin.adminName
        gCurrentUser.employee = True
        gCurrentUser.email = admin.emailAdmin

        if admin and bcrypt.check_password_hash(admin.passwordAdmin, form.passwordAdmin.data):
            app.logger.info('admin login  successful')
            flash(f'Welcome {admin.adminName}')
            return render_template('employeeSelection.html')
    return render_template('adminLogin.html', form=form)


@app.route('/employeeHome')
def employeeHome():
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    return render_template('employeeHome.html')

@app.route('/adminHome')
def adminHome():
    query = request.args.get('queries')
    if query:
          results = []
          #app.logger.info('here')
          for i in range(len(movieList)):
             if query.lower() in movieList[i].title.lower() or movieList[i].genre in query.lower() or query.lower() in movieList[i].dates:
                results.append(movieList[i])
          #app.logger.info('result',results[0].title)      
          return render_template('search_results.html', results=results)
    return render_template('adminHome.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
