from table import Table
from models import Reservation

class ReservationTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                reservationID INTEGER PRIMARY KEY AUTOINCREMENT,
                resource INT,
                start TEXT,
                end TEXT,
                FOREIGN KEY(resource) REFERENCES resources(resourceID))''')
        self.connection.commit()
        
    def save(self, reservation):
        if reservation.ID:
            self.cursor.execute('UPDATE reservations SET resource=?, start=?, end=? WHERE reservationID=?', reservation.get_data())
            self.connection.commit()
        else:
            self.cursor.execute('INSERT INTO reservations(resource, start, end) VALUES (?,?,?)', reservation.get_data())
            self.connection.commit()
            reservation.ID = self.cursor.lastrowid

    def get_all(self):
        self.cursor.execute('SELECT * FROM reservations')
        rows = self.cursor.fetchall()
        return rows

    def get_by_date(self, date):
        self.cursor.execute('SELECT * FROM reservations WHERE ? BETWEEN date(start) and date(end)', (date,))
        rows = self.cursor.fetchall()
        return rows

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS reservations')
        self.connection.commit()
        self = ReservationTable(self.connection)

