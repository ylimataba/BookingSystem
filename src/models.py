class Model():
    def __init__(self):
        self.ID = None

    def get_data(self):
        pass

    def __lt__(self, other):
        return self.ID < other.ID

    def __le__(self, other):
        return self.ID <= other.ID

    def __eq__(self, other):
        return self.ID == other.ID

    def __ne__(self, other):
        return self.ID != other.ID

    def __gt__(self, other):
        return self.ID > other.ID

    def __ge__(self, other):
        return self.ID >= other.ID

class Reservation(Model):
    def __init__(self, ID=None, customer=None, resource=None, date=None,
            start=None, end=None, services=None, row=None):
        super().__init__()
        if row:
            self.ID = row[0]
            #self.resource = Resource(ID=row[1])
            self.date = row[1]
            self.start = row[2]
            self.end = row[3]
        else:
            self.ID = ID
            #self.customer = customer
            #self.resource = resource
            self.date = date
            self.start = start
            self.end = end
            #self.services = services

    def get_data(self):
        if self.ID:
            data = (self.date, self.start, self.end, self.ID)
        else:
            data = (self.date, self.start, self.end)
        return data
    
    def __str__(self):
        return "Reservation(ID: {0}, date: {1}, start: {2}, end: {3})".format(self.ID,self.date, self.start, self.end)

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
