import unittest
from PyQt5 import QtWidgets, QtCore, QtGui

from models import Reservation
from database import Database
from database_error import DatabaseError

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database('test.db')
        self.db.reset()

    def test_get_all_reservations(self):
        added_reservations = []
        date = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
        for x in range(8,19):
            start_time = QtCore.QTime(x,0).toString("hh.mm")
            end_time = QtCore.QTime(x+1,0).toString("hh.mm")
            new_reservation = Reservation(date=date, start=start_time, end=end_time)
            self.db.save(new_reservation)
            added_reservations.append(new_reservation)
        reservations = self.db.reservations.get_all()
        for i in range(len(reservations)):
            self.assertEqual(reservations[i], added_reservations[i])




if __name__ == '__main__':
    unittest.main()
