import sqlite3
from database_error import DatabaseError
from reservation_table import ReservationTable

class Database:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.reservations = ReservationTable(self.connection)

    def reset(self):
        self.reservations.reset()
