from table import Table
from models import Reservation

class ReservationTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                reservationID INTEGER PRIMARY KEY AUTOINCREMENT,
                customer INT,
                resource INT,
                start TEXT,
                end TEXT,
                FOREIGN KEY(customer) REFERENCES customers(customerID),
                FOREIGN KEY(resource) REFERENCES resources(resourceID))''')
        self.connection.commit()
        
    def save(self, reservation):
        if self.is_free(reservation):
            if reservation.ID:
                self.cursor.execute('UPDATE reservations SET customer=?, resource=?, start=?, end=? WHERE reservationID=?', reservation.get_data())
                self.connection.commit()
            else:
                self.cursor.execute('INSERT INTO reservations(customer, resource, start, end) VALUES (?,?,?,?)', reservation.get_data())
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
        self.cursor.execute('''SELECT resource FROM reservations
                WHERE resource=? 
                AND (start BETWEEN ? AND ?
                OR end BETWEEN ? AND ?)
                OR (resource=? AND start <= ? AND end >= ?)''',
                (reservation.resource.ID,start,end,start,end,reservation.resource.ID,start,end))
        rows = self.cursor.fetchall()
        if reservation.ID:
            if len(rows) == 1:
                if rows[0][0] == reservation.ID:
                    return True
        if len(rows) > 0:
            return False
        return True

    def delete(self, reservation):
        self.cursor.execute('DELETE FROM reservations WHERE reservationID=?', (reservation.ID,))
        self.connection.commit()

    def delete_by_resource_id(self, resourceID):
        self.cursor.execute('DELETE FROM reservations WHERE resource=?', (resourceID,))
        self.connection.commit()
    
    def delete_by_customer_id(self, customerID):
        self.cursor.execute('DELETE FROM reservations WHERE customer=?', (customerID,))
        self.connection.commit()

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS reservations')
        self.connection.commit()
        self = ReservationTable(self.connection)

