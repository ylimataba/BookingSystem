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

    def new_reservation(self, resource, start, end):
        if self.resources.is_free(resource.ID, start.toString('yyyy-MM-dd hh:mm'), end.toString('yyyy-MM-dd hh:mm')):
            reservation = Reservation(resource=resource,start=start,end=end)
            self.save(reservation)
            return reservation
        else:
            return None

    def get_reservations(self, date=None):
        try:
            reservations = []
            if date:
                reservation_rows = self.reservations.get_by_date(date.toString('yyyy-MM-dd'))
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
    
    def get_start_and_end(self, date):
        try:
            reservations = self.get_reservations(date=date)
            if reservations:
                start = reservations[0].get_start_time_on_date(date)
                reservations.sort(key=lambda x: x.get_end_time_on_date(date), reverse=True)
                end = reservations[0].get_end_time_on_date(date)
                return (int(start // 1), int(-(-end // 1) +1))
            else:
                return (None, None)
        except Exception as e:
            raise DatabaseError(str(e))

    def save(self, object_to_save):
        try:
            if type(object_to_save) is Reservation:
                self.resources.save(object_to_save.resource)
                return self.reservations.save(object_to_save)
            elif type(object_to_save) is Resource:
                return self.resources.save(object_to_save)
        except Exception as e:
            raise DatabaseError(str(e))

    def reset(self):
        try:
            self.resources.reset()
            self.reservations.reset()
        except Exception as e:
            raise DatabaseError(str(e))
