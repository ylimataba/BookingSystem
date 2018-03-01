import sqlite3
from model import Model

class Reservation(Model):
    def __init__(self, ID=None, customer=None, resource=None, start=None,
            end=None, services=None, row=None):
        super().__init__()
        if row:
            self.ID = row[0]
            self.start = row[1]
            self.end = row[2]
        else:
            self.ID = ID
            #self.customer = customer
            #self.resource = resource
            self.start = start
            self.end = end
            #self.services = services

    def save(self, database):
        data = (self.ID, self.start, self.end)
        database.insert_into_reservations(data)
    
    def __str__(self):
        return "Reservation(ID: {0}, start: {1}, end: {2})".format(self.ID, self.start, self.end)
