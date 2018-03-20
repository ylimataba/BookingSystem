from PyQt5 import QtCore

class Model():
    def __init__(self):
        self.ID = None

    def get_data(self):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

class Reservation(Model):
    def __init__(self, ID=None, customer=None, resource=None, date=None,
            start=None, end=None, services=None, row=None):
        super().__init__()
        #self.customer = customer
        self.resource = resource
        #self.services = services
        if row:
            self.ID = row[0]
            self.date = QtCore.QDate.fromString(row[2], 'yyyy-MM-dd')
            self.start = QtCore.QTime.fromString(row[3], 'hh.mm')
            self.end = QtCore.QTime.fromString(row[4], 'hh.mm')
        else:
            self.ID = ID
            self.date = date
            self.start = start
            self.end = end

    def get_data(self):
        if self.ID:
            data = (self.resource.ID, self.date.toString('yyyy-MM-dd'), self.start.toString('hh.mm'), self.end.toString('hh.mm'), self.ID)
        else:
            data = (self.resource.ID, self.date.toString('yyyy-MM-dd'), self.start.toString('hh.mm'), self.end.toString('hh.mm'))
        return data

    def to_html(self):
        return "{0}<br>{1}<br>{2} - {3}".format(
                self.resource.name,
                self.date.toString('dd.MM.yyyy'),
                self.start.toString('hh.mm'),
                self.end.toString('hh.mm'))

    
    def __str__(self):
        return "Reservation(ID: {0}, resourceID: {1}, date: {2}, start: {3}, end: {4})".format(
                self.ID,
                self.resource.ID,
                self.date.toString('yyyy-MM-dd'),
                self.start.toString('hh.mm'),
                self.end.toString('hh.mm'))

class Resource(Model):
    def __init__(self, ID=None, name=None, resource_type=None, row=None):
        super().__init__()
        if row:
            self.ID = row[0]
            self.name = row[1]
            self.resource_type = row[2]
        else:
            self.ID = ID
            self.name = name
            self.resource_type = resource_type

    def get_data(self):
        if self.ID:
            data = (self.name, self.resource_type, self.ID)
        else:
            data = (self.name, self.resource_type)
        return data
    
    def __str__(self):
        return "Resource(ID: {0}, name: {1}, type: {2})".format(self.ID, self.name, self.resource_type)
