import sqlite3
from database_error import DatabaseError
from reservation_table import ReservationTable
from resource_table import ResourceTable
from models import Reservation, Resource

class Database:
    def __init__(self, filename="default.db"):
        self.connection = sqlite3.connect(filename)
        self.reservations = ReservationTable(self.connection)
        self.resources = ResourceTable(self.connection)

    def save(self, object_to_save):
        if type(object_to_save) is Reservation:
            self.reservations.save(object_to_save)
        elif type(object_to_save) is Resource:
            self.resources.save(object_to_save)

    def reset(self):
        self.reservations.reset()
        self.resources.reset()
