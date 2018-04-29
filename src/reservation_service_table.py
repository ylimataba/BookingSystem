from table import Table
from models import Service

class ReservationServiceTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservationservices (
                reservationserviceID INTEGER PRIMARY KEY AUTOINCREMENT,
                service INT,
                reservation INT,
                FOREIGN KEY(service) REFERENCES services(serviceID),
                FOREIGN KEY(reservation) REFERENCES reservations(reservationID))''')
        self.connection.commit()
        
    def save(self, reservation):
        self.delete_by_reservation_id(reservation.ID)
        for service in reservation.services:
            self.cursor.execute('INSERT INTO reservationservices(service, reservation) VALUES (?,?)', (service.ID, reservation.ID))
            self.connection.commit()
        return True

    def delete_by_reservation_id(self, reservationID):
        self.cursor.execute('DELETE FROM reservationservices WHERE reservation=?', (reservationID,))
        self.connection.commit()

    def delete_by_service_id(self, serviceID):
        self.cursor.execute('DELETE FROM reservationservices WHERE service=?', (serviceID,))
        self.connection.commit()

    def get_by_reservation_id(self, reservationID):
        self.cursor.execute('SELECT * FROM reservationservices WHERE reservation=?', (reservationID,))
        rows = self.cursor.fetchall()
        return rows

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS reservationservices')
        self.connection.commit()
        self = ReservationServiceTable(self.connection)

