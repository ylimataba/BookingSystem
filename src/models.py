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
            start=None, end=None, services=[], row=None):
        super().__init__()
        self.customer = customer
        self.resource = resource
        self.services = services
        if row:
            self.ID = row[0]
            self.start = QtCore.QDateTime.fromString(row[3], 'yyyy-MM-dd hh:mm')
            #self.end = self.start.addSecs(self.get_duration() * 60)
            self.end = QtCore.QDateTime.fromString(row[4], 'yyyy-MM-dd hh:mm')
        else:
            self.ID = ID
            self.start = start
            self.end = end

    def get_data(self):
        if self.ID:
            data = (self.customer.ID, self.resource.ID, self.start.toString('yyyy-MM-dd hh:mm'), self.end.toString('yyyy-MM-dd hh:mm'), self.ID)
        else:
            data = (self.customer.ID, self.resource.ID, self.start.toString('yyyy-MM-dd hh:mm'), self.end.toString('yyyy-MM-dd hh:mm'))
        return data

    def to_html(self):
        return "{0}<br>{1} - {2}".format(
                self.customer.name,
                self.start.toString('yyyy-MM-dd hh:mm'),
                self.end.toString('yyyy-MM-dd hh:mm'))

    def get_start_time_on_date(self, date):
        if self.start.date() == date:
            msecs = self.start.time().msecsSinceStartOfDay()
            return msecs / 3600000
        else:
            return 0

    def get_end_time_on_date(self, date):
        if self.end.date() == date:
            msecs = self.end.time().msecsSinceStartOfDay()
            return msecs / 3600000
        else:
            return 24
    
    def get_duration_on_date(self, date):
        return self.get_end_time_on_date(date) - self.get_start_time_on_date(date)

    def get_duration(self):
        duration = 0
        for service in self.services:
            duration += service.duration
        return duration

    def get_price(self):
        price = 0
        for service in self.services:
            price += service.price
        return price
    
    def __str__(self):
        return "Reservation(ID: {0}, resourceID: {1}, start: {2}, end: {3})".format(
                self.ID,
                self.resource.ID,
                self.start.toString('yyyy-MM-dd hh:mm'),
                self.end.toString('yyyy-MM-dd hh:mm'))

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

class Service(Model):
    def __init__(self, ID=None, name=None, price=None, duration=None, description=None, row=None):
        super().__init__()
        if row:
            self.ID = row[0]
            self.name = row[1]
            self.price = row[2]
            self.duration = row[3]
            self.description = row[4]
        else:
            self.ID = ID
            self.name = name
            self.price = price
            self.duration = duration
            self.description = description
    
    def get_data(self):
        if self.ID:
            data = (self.name, self.price, self.duration, self.description, self.ID)
        else:
            data = (self.name, self.price, self.duration, self.description)
        return data

    def __str__(self):
        return "Service(ID: {0}, name: {1}, price: {2}, duration: {3}, description: {4})".format(self.ID, self.name, self.price, self.duration, self.description)

class Customer(Model):
    def __init__(self, ID=None, name=None, email=None, row=None):
        super().__init__()
        if row:
            self.ID = row[0]
            self.name = row[1]
            self.email = row[2]
        else:
            self.ID = ID
            self.name = name
            self.email = email

    def get_data(self):
        if self.ID:
            data = (self.name, self.email, self.ID)
        else:
            data = (self.name, self.email)
        return data

    def __str__(self):
        return "Customer(ID: {0}, name: {1}, email: {2})".format(self.ID, self.name, self.email) 


