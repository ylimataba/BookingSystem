import unittest
from PyQt5 import QtWidgets, QtCore, QtGui

from models import Reservation, Resource, Service, Customer
from database import Database
from database_error import DatabaseError

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database('test.db')
        self.db.reset()

    def test_reservations_by_customer(self):
        customer = Customer(name='Teemu Teekkari', email='teemu.teekkari@aalto fi')
        service1 = Service(name='service1',price=10.0,duration=60.0,description='service1 description')
        service2 = Service(name='service1',price=10.0,duration=60.0,description='service1 description')
        self.db.save(service1)
        self.db.save(service2)
        added_reservations = []
        date = QtCore.QDate.currentDate()
        resource = Resource(name="Resource1", resource_type="ROOM")
        for x in range(8,19):
            start_time = QtCore.QTime(x,0)
            end_time = QtCore.QTime(x,59)
            start = QtCore.QDateTime(date,start_time)
            end = QtCore.QDateTime(date, end_time)
            new_reservation = Reservation(customer=customer, resource=resource, start=start, end=end, services=[service1,service2])
            self.db.save(new_reservation)
            added_reservations.append(new_reservation)
        reservations = self.db.get_reservations(customer=customer)
        for i in range(len(reservations)):
            self.assertEqual(reservations[i], added_reservations[i])

    def test_get_customers(self):
        customer1 = Customer(name="Teemu Teekkari", email="teemu.teekkari@aalto.fi")
        customer2 = Customer(name="Tiina Teekkari", email="tiina.teekkari@aalto.fi")
        self.db.save(customer1)
        self.db.save(customer2)
        customers = self.db.get_customers()
        self.assertEqual(customers,[customer1,customer2])
    
    def test_get_services(self):
        service1 = Service(name='service1',price=10.0,duration=60.0,description='service1 description')
        service2 = Service(name='service1',price=10.0,duration=60.0,description='service1 description')
        self.db.save(service1)
        self.db.save(service2)
        services = self.db.get_services()
        self.assertEqual(services, [service1,service2])

    def test_get_reservations(self):
        customer = Customer(name='Teemu Teekkari', email='teemu.teekkari@aalto fi')
        service1 = Service(name='service1',price=10.0,duration=60.0,description='service1 description')
        service2 = Service(name='service1',price=10.0,duration=60.0,description='service1 description')
        self.db.save(service1)
        self.db.save(service2)
        added_reservations = []
        date = QtCore.QDate.currentDate()
        resource = Resource(name="Resource1", resource_type="ROOM")
        for x in range(8,19):
            start_time = QtCore.QTime(x,0)
            end_time = QtCore.QTime(x,59)
            start = QtCore.QDateTime(date,start_time)
            end = QtCore.QDateTime(date, end_time)
            new_reservation = Reservation(customer=customer, resource=resource, start=start, end=end, services=[service1,service2])
            self.db.save(new_reservation)
            added_reservations.append(new_reservation)
        reservations = self.db.get_reservations()
        for i in range(len(reservations)):
            self.assertEqual(reservations[i], added_reservations[i])
    
    def test_model_eq(self):
        resource1 = Resource(ID=1, name="Resource1", resource_type="ROOM")
        resource2 = Resource(ID=1, name="Resource1", resource_type="ROOM")
        resource3 = Resource(ID=1, name="Resource3", resource_type="ROOM")
        self.assertEqual(resource1, resource2)
        self.assertNotEqual(resource1, resource3)
        
        date = QtCore.QDate.currentDate()
        start_time = QtCore.QTime(8,0)
        end_time = QtCore.QTime(9,0)
        start = QtCore.QDateTime(date,start_time)
        end = QtCore.QDateTime(date, end_time)
        reservation1 = Reservation(ID=1, resource=resource1, start=start, end=end)
        reservation2 = Reservation(ID=1, resource=resource2, start=start, end=end)
        reservation3 = Reservation(ID=1, resource=resource3, start=start, end=end)
        self.assertEqual(reservation1, reservation2)
        self.assertNotEqual(reservation1, reservation3)

    def test_resource_creation(self):
        resource = Resource(name="Resource1", resource_type="ROOM")
        self.db.save(resource)
        resource_from_db = self.db.resources.get_by_id(resource.ID)
        self.assertEqual(resource, resource_from_db)

    def test_service_creation(self):
        service = Service(name='service1',price=10.0,duration=60.0,description='service1 description')
        self.db.save(service)
        service_from_db = self.db.services.get_by_id(service.ID)
        self.assertEqual(service, service_from_db)

    def test_is_free(self): # change resources.is_free to reservations.is_free
        customer = Customer(name='Teemu Teekkari', email='teemu.teekkari@aalto fi')
        resource = Resource(name="Resource1", resource_type="ROOM")
        date = QtCore.QDate(2018,3,8)
        start_time = QtCore.QTime(10,0)
        end_time = QtCore.QTime(11,0)
        start = QtCore.QDateTime(date,start_time)
        end = QtCore.QDateTime(date, end_time)
        reservation = Reservation(customer=customer, resource=resource, start=start, end=end)
        self.db.save(reservation)
        self.assertEqual(self.db.reservations.is_free(2,'2018-03-08 10:00','2018-03-08 11:00'), True)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-07 10:00','2018-03-07 11:00'), True)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-08 09:00','2018-03-08 09:59'), True)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-08 11:01','2018-03-08 12:00'), True)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-08 10:00','2018-03-08 11:00'), False)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-08 09:00','2018-03-08 11:00'), False)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-08 09:00','2018-03-08 10:30'), False)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-08 10:30','2018-03-08 12:00'), False)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-08 09:00','2018-03-08 14:00'), False)
        self.assertEqual(self.db.reservations.is_free(1,'2018-03-08 10:30','2018-03-08 10:59'), False)
        self.assertEqual(self.db.reservations.is_free(reservation.resource.ID,reservation.start.toString('yyyy-MM-dd hh:mm'),reservation.end.toString('yyyy-MM-dd hh:mm'),reservationID=reservation.ID), True)

    def test_get_reservations_by_date(self):
        customer = Customer(name='Teemu Teekkari', email='teemu.teekkari@aalto fi')
        added_reservations = []
        date = QtCore.QDate.currentDate()
        resource = Resource(name="Resource1", resource_type="ROOM")
        for x in range(19,8):
            start_time = QtCore.QTime(x,0)
            end_time = QtCore.QTime(x-1,0)
            start = QtCore.QDateTime(date,start_time)
            end = QtCore.QDateTime(date, end_time)
            new_reservation = Reservation(customer=customer, resource=resource, start=start, end=end)
            self.db.save(new_reservation)
            added_reservations.append(new_reservation)
        reservations = self.db.get_reservations(date=date)
        for i in range(len(reservations)):
            self.assertEqual(reservations[len(reservations)-i-1], added_reservations[i])

    def test_get_start_and_end(self):
        customer = Customer(name='Teemu Teekkari', email='teemu.teekkari@aalto fi')
        date = QtCore.QDate.currentDate()
        resource = Resource(name="Resource1", resource_type="ROOM")
        for x in range(8,19):
            start_time = QtCore.QTime(x,0)
            end_time = QtCore.QTime(x+1,0)
            start = QtCore.QDateTime(date,start_time)
            end = QtCore.QDateTime(date, end_time)
            new_reservation = Reservation(customer=customer, resource=resource, start=start, end=end)
            self.db.save(new_reservation)
        (first, last) = self.db.get_start_and_end(date)
        self.assertEqual(first, 8)
        self.assertEqual(last, 20)

if __name__ == '__main__':
    unittest.main()
