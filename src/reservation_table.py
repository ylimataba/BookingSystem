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
        if self.is_free(reservation):
            if reservation.ID:
                self.cursor.execute('UPDATE reservations SET resource=?, start=?, end=? WHERE reservationID=?', reservation.get_data())
                self.connection.commit()
            else:
                self.cursor.execute('INSERT INTO reservations(resource, start, end) VALUES (?,?,?)', reservation.get_data())
                self.connection.commit()
                reservation.ID = self.cursor.lastrowid
            return True
        return False

    def get_all(self):
        self.cursor.execute('SELECT * FROM reservations')
        rows = self.cursor.fetchall()
        return rows

    def get_by_date(self, date):
        self.cursor.execute('SELECT * FROM reservations WHERE ? BETWEEN date(start) and date(end) ORDER BY start', (date,))
        rows = self.cursor.fetchall()
        return rows

    def is_free(self, reservation):
        start = reservation.start.toString('yyyy-MM-dd hh:mm')
        end = reservation.end.toString('yyyy-MM-dd hh:mm')
        self.cursor.execute('''SELECT * FROM reservations
                WHERE resource=? 
                AND (start BETWEEN ? AND ?
                OR end BETWEEN ? AND ?)''',
                (reservation.resource.ID,start,end,start,end))
        rows = self.cursor.fetchall()
        if reservation.ID:
            if len(rows) == 1:
                if rows[0][0] == reservation.ID:
                    return True
        if len(rows) > 0:
            return False
        return True

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS reservations')
        self.connection.commit()
        self = ReservationTable(self.connection)

