class Model():
    def __init__(self):
        self.ID = None

    def save(self):
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
