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

    def new_reservation(self, resource, date, start, end):
        if self.resources.is_free(resource.ID, date.toString('yyyy-MM-dd'), start.toString('hh.mm'), end.toString('hh.mm')):
            reservation = Reservation(resource=resource,date=date,start=start,end=end)
            return reservation
        else:
            return None

    def get_reservations(self, date=None):
        try:
            reservations = []
            if date:
                reservation_rows = self.reservations.get_by_date(date)
            else:
                reservation_rows = self.reservations.get_all()
            for row in reservation_rows:
                resource = self.resources.get_by_id(row[1])
                reservations.append(Reservation(row=row, resource=resource))
            return reservations
        except Exception as e:
            raise DatabaseError(str(e))

    def get_resources(self, ID=None):
        try:
            if ID:
                return self.resources.get_by_id(ID)
            else:
                return self.resources.get_all()
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
