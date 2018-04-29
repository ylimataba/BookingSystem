import sqlite3
from database_error import DatabaseError
from reservation_table import ReservationTable
from resource_table import ResourceTable
from service_table import ServiceTable
from reservation_service_table import ReservationServiceTable
from customer_table import CustomerTable
from models import Reservation, Resource, Service, Customer

class Database:
    def __init__(self, filename="default.db"):
        try:
            self.connection = sqlite3.connect(filename)
            self.resources = ResourceTable(self.connection)
            self.reservations = ReservationTable(self.connection)
            self.services = ServiceTable(self.connection)
            self.customers = CustomerTable(self.connection)
            self.reservationservices = ReservationServiceTable(self.connection)
        except Exception as e:
            raise DatabaseError(str(e))

    def get_reservations(self, date=None):
        try:
            reservations = []
            if date:
                reservation_rows = self.reservations.get_by_date(date.toString('yyyy-MM-dd'))
            else:
                reservation_rows = self.reservations.get_all()
            for row in reservation_rows:
                customer = self.customers.get_by_id(row[1])
                resource = self.resources.get_by_id(row[2])
                rservices = self.get_services(reservationID=row[0])
                reservations.append(Reservation(row=row, customer=customer, resource=resource, services=rservices))
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

    def get_services(self, reservationID=None, ID=None):
        try:
            if reservationID:
                rservices = []
                service_id_rows = self.reservationservices.get_by_reservation_id(reservationID)
                for row in service_id_rows:
                    rservices.append(self.get_services(ID=row[1]))
                return rservices
            elif ID:
                return self.services.get_by_id(ID)
            else:
                return self.services.get_all()
        except Exception as e:
            raise DatabaseError(str(e))
    
    def get_customers(self, ID=None):
        try:
            if ID:
                return self.customers.get_by_id(ID)
            else:
                return self.customers.get_all()
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
                self.customers.save(object_to_save.customer)
                self.resources.save(object_to_save.resource)
                if self.reservations.save(object_to_save):
                    self.reservationservices.save(object_to_save)
                    return True
                else:
                    return False
            elif type(object_to_save) is Resource:
                return self.resources.save(object_to_save)
            elif type(object_to_save) is Service:
                return self.services.save(object_to_save)
            elif type(object_to_save) is Customer:
                return self.customers.save(object_to_save)
        except Exception as e:
            raise DatabaseError(str(e))

    def reset(self):
        try:
            self.resources.reset()
            self.reservations.reset()
            self.services.reset()
            self.reservationservices.reset()
            self.customers.reset()
        except Exception as e:
            raise DatabaseError(str(e))
