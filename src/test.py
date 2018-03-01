import unittest
import datetime

from reservation import Reservation
from database import Database
from database_error import DatabaseError

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database('test.db')
        self.db.reset()

    def test_get_all_reservations(self):
        added_reservations = []
        for x in range(8,19):
            start_time = datetime.datetime(2018,2,28,x)
            end_time = datetime.datetime(2018,2,28,x+1)
            new_reservation = Reservation(ID=x-7, start=start_time, end=end_time)
            new_reservation.save(self.db)
            added_reservations.append(new_reservation)
        reservations = self.db.get_all_reservations()
        for i in range(len(reservations)):
            self.assertEqual(reservations[i], added_reservations[i])




if __name__ == '__main__':
    unittest.main()
