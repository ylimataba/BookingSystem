class Table:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def insert(self, data):
        pass

    def update(self, data):
        pass

    def get_all(self, data):
        pass

    def reset(self):
        pass
