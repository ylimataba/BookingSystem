import sqlite3
from database_error import DatabaseError
from reservation import Reservation

class Database:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.create_reservation_table()

    def create_reservation_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS reservations (reservationID INTEGER PRIMARY KEY, start TEXT, end TEXT)')
        self.connection.commit()
        
    def insert_into_reservations(self, data):
        try:
            self.cursor.execute('INSERT INTO reservations VALUES (?,?,?)', data)
            self.connection.commit()
        except Exception as e:
            raise DatabaseError(str(e))

    def get_all_reservations(self):
        reservations = []
        self.cursor.execute('SELECT * FROM reservations')
        rows = self.cursor.fetchall()
        for row in rows:
            reservations.append(Reservation(row=row))
        return reservations

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS reservations')
        self.create_reservation_table()
        self.connection.commit()
