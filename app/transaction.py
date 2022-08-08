import datetime
from datetime import date

#Class used to creat transaction objects
#Holds the details of the current transaction to be written to the database

class Transaction:
    customerName = ""
    movie = ""
    showDate = date(2020, 1, 1)
    showTime = datetime.time(0,0,0)
    bookDate = date(2020, 1, 1)
    email = ""
    aQuantity = 0
    sQuantity = 0
    cQuantity = 0
    total = 0.0

    def __init__(self, customerName, movie, showDate, showTime, bookDate, email, aQuantity, sQuantity, cQuantity, total):
        self.customerName = customerName
        self.movie = movie
        self.showDate = showDate
        self.showTime = showTime
        self.bookDate = bookDate
        self.email = email
        self.aQuantity = aQuantity
        self.sQuantity = sQuantity
        self.cQuantity = cQuantity
        self.total = total
        
    def calculateTotal(self):
        self.total = self.aQuantity*10 + self.sQuantity*6 + self.cQuantity*6
        return self.total

    def totalNoOfTickets(self):
        return self.aQuantity + self.sQuantity + self.cQuantity

    def setShowTime(self, stringTime):
        self.showTime = datetime.datetime.strptime(stringTime, '%H:%M').time()
        return self.showTime

