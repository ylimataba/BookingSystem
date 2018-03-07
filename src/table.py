class Table:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def save(self, objct):
        pass

    def get_all(self):
        pass

    def reset(self):
        pass
