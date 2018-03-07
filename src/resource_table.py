from table import Table
from models import Resource

class ResourceTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('CREATE TABLE IF NOT EXISTS resources (resourceID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT)')
        self.connection.commit()
        
    def save(self, resource):
        try:
            if resource.ID:
                self.cursor.execute('UPDATE resources SET name=?, type=? WHERE resourceID=?', reservation.get_data())
            else:
                self.cursor.execute('INSERT INTO reservations(name, type) VALUES (?,?)', reservation.get_data())
            self.connection.commit()
            resource.ID = self.cursor.lastrowid
        except Exception as e:
            raise DatabaseError(str(e))

    def get_all(self):
        resources = []
        self.cursor.execute('SELECT * FROM resources')
        rows = self.cursor.fetchall()
        for row in rows:
            resources.append(Resource(row=row))
        return resources

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS resources')
        self.connection.commit()
        self = ResourceTable(self.connection)

