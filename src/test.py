import unittest
from PyQt5 import QtWidgets, QtCore, QtGui

from models import Reservation, Resource
from database import Database
from database_error import DatabaseError

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database('test.db')
        self.db.reset()
    
    def test_model_eq(self):
        resource1 = Resource(ID=1, name="Resource1", resource_type="ROOM")
        resource2 = Resource(ID=1, name="Resource1", resource_type="ROOM")
        resource3 = Resource(ID=1, name="Resource3", resource_type="ROOM")
        self.assertEqual(resource1, resource2)
        self.assertNotEqual(resource1, resource3)
        
        date = QtCore.QDate.currentDate()
        start_time = QtCore.QTime(8,0)
        end_time = QtCore.QTime(9,0)
        reservation1 = Reservation(ID=1, resource=resource1, date=date, start=start_time, end=end_time)
        reservation2 = Reservation(ID=1, resource=resource2, date=date, start=start_time, end=end_time)
        reservation3 = Reservation(ID=1, resource=resource3, date=date, start=start_time, end=end_time)
        self.assertEqual(reservation1, reservation2)
        self.assertNotEqual(reservation1, reservation3)

    def test_resource_creation(self):
        resource = Resource(name="Resource1", resource_type="ROOM")
        self.db.save(resource)
        resource_from_db = self.db.resources.get_by_id(resource.ID)
        self.assertEqual(resource, resource_from_db)

    def test_get_reservations(self):
        added_reservations = []
        date = QtCore.QDate.currentDate()
        resource = Resource(name="Resource1", resource_type="ROOM")
        for x in range(8,19):
            start_time = QtCore.QTime(x,0)
            end_time = QtCore.QTime(x+1,0)
            new_reservation = Reservation(resource=resource, date=date, start=start_time, end=end_time)
            self.db.save(new_reservation)
            added_reservations.append(new_reservation)
        reservations = self.db.get_reservations()
        for i in range(len(reservations)):
            self.assertEqual(reservations[i], added_reservations[i])




if __name__ == '__main__':
    unittest.main()
