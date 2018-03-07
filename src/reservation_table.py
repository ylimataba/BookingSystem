from table import Table
from models import Reservation

class ReservationTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('CREATE TABLE IF NOT EXISTS reservations (reservationID INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, start TEXT, end TEXT)')
        self.connection.commit()
        
    def save(self, reservation):
        try:
            if reservation.ID:
                self.cursor.execute('UPDATE reservations SET date=?, start=?, end=? WHERE reservationID=?', reservation.get_data())
            else:
                self.cursor.execute('INSERT INTO reservations(date, start, end) VALUES (?,?,?)', reservation.get_data())
            self.connection.commit()
            reservation.ID = self.cursor.lastrowid
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

