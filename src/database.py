import sqlite3
from database_error import DatabaseError
from reservation_table import ReservationTable
from resource_table import ResourceTable
from models import Reservation, Resource

class Database:
    def __init__(self, filename="default.db"):
        try:
            self.connection = sqlite3.connect(filename)
            self.resources = ResourceTable(self.connection)
            self.reservations = ReservationTable(self.connection)
        except Exception as e:
            raise DatabaseError(str(e))

    def get_reservations(self):
        try:
            reservations = []
            reservation_rows = self.reservations.get_all()
            for row in reservation_rows:
                resource = self.resources.get_by_id(row[1])
                reservations.append(Reservation(row=row, resource=resource))
            return reservations
        except Exception as e:
            raise DatabaseError(str(e))

    def save(self, object_to_save):
        try:
            if type(object_to_save) is Reservation:
                self.resources.save(object_to_save.resource)
                self.reservations.save(object_to_save)
            elif type(object_to_save) is Resource:
                self.resources.save(object_to_save)
        except Exception as e:
            raise DatabaseError(str(e))

    def reset(self):
        try:
            self.resources.reset()
            self.reservations.reset()
        except Exception as e:
            raise DatabaseError(str(e))
