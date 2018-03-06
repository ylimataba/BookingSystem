import sqlite3
from model import Model

class Reservation(Model):
    def __init__(self, ID=None, customer=None, resource=None, date=None,
            start=None, end=None, services=None, row=None):
        super().__init__()
        if row:
            self.ID = row[0]
            self.date = row[1]
            self.start = row[2]
            self.end = row[3]
        else:
            self.ID = ID
            #self.customer = customer
            #self.resource = resource
            self.date = date
            self.start = start
            self.end = end
            #self.services = services

    def save(self, reservations):
        if self.ID:
            data = (self.date, self.start, self.end, self.ID)
            reservations.update(data)
        else:
            data = (self.date, self.start, self.end)
            self.ID = reservations.insert(data)
    
    def __str__(self):
        return "Reservation(ID: {0}, date: {1}, start: {2}, end: {3})".format(self.ID,self.date, self.start, self.end)
