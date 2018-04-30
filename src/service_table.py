from table import Table
from models import Service

class ServiceTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('CREATE TABLE IF NOT EXISTS services (serviceID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, duration REAL, description TEXT)')
        self.connection.commit()
        
    def save(self, service):
        if service.ID:
            self.cursor.execute('''UPDATE services SET name=?,
                    price=?,
                    duration=?,
                    description=?
                    WHERE serviceID=?''', service.get_data())
            self.connection.commit()
        else:
            self.cursor.execute('INSERT INTO services(name, price, duration, description) VALUES (?,?,?,?)', service.get_data())
            self.connection.commit()
            service.ID = self.cursor.lastrowid
        return True

    def get_all(self):
        services = []
        self.cursor.execute('SELECT * FROM services ORDER BY name COLLATE NOCASE')
        rows = self.cursor.fetchall()
        for row in rows:
            services.append(Service(row=row))
        return services

    def get_by_id(self, ID):
        self.cursor.execute('SELECT * FROM services WHERE serviceID=?', (ID,))
        row = self.cursor.fetchone()
        service = Service(row=row)
        return service

    def delete(self, service):
        self.cursor.execute('DELETE FROM services WHERE serviceID=?', (service.ID,))
        self.connection.commit()

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS services')
        self.connection.commit()
        self = ServiceTable(self.connection)

