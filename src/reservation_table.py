from table import Table
from reservation import Reservation

class ReservationTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('CREATE TABLE IF NOT EXISTS reservations (reservationID INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, start TEXT, end TEXT)')
        self.connection.commit()
        
    def insert(self, data):
        try:
            self.cursor.execute('INSERT INTO reservations(date, start, end) VALUES (?,?,?)', data)
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            raise DatabaseError(str(e))

    def update(self, data):
        try:
            self.cursor.execute('UPDATE reservations SET date=?, start=?, end=? WHERE reservationID=?', data)
            self.connection.commit()
        except Exception as e:
            raise DatabaseError(str(e))

    def get_all(self):
        reservations = []
        self.cursor.execute('SELECT * FROM reservations')
        rows = self.cursor.fetchall()
        for row in rows:
            reservations.append(Reservation(row=row))
        return reservations

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS reservations')
        self.connection.commit()
        self = ReservationTable(self.connection)

