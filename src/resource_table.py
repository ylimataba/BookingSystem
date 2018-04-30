from table import Table
from models import Resource

class ResourceTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('CREATE TABLE IF NOT EXISTS resources (resourceID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT)')
        self.connection.commit()
        
    def save(self, resource):
        if resource.ID:
            self.cursor.execute('UPDATE resources SET name=?, type=? WHERE resourceID=?', resource.get_data())
            self.connection.commit()
        else:
            self.cursor.execute('INSERT INTO resources(name, type) VALUES (?,?)', resource.get_data())
            self.connection.commit()
            resource.ID = self.cursor.lastrowid
        return True

    def get_all(self):
        resources = []
        self.cursor.execute('SELECT * FROM resources ORDER BY name COLLATE NOCASE')
        rows = self.cursor.fetchall()
        for row in rows:
            resources.append(Resource(row=row))
        return resources

    def get_by_id(self, ID):
        self.cursor.execute('SELECT * FROM resources WHERE resourceID=?', (ID,))
        resource = Resource(row=self.cursor.fetchone())
        return resource

    def delete(self, resource):
        self.cursor.execute('DELETE FROM resources WHERE resourceID=?', (resource.ID,))
        self.connection.commit()

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS resources')
        self.connection.commit()
        self = ResourceTable(self.connection)

