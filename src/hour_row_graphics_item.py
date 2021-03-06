from PyQt5 import QtWidgets, QtCore, QtGui
from models import Reservation, Resource

class HourRowGraphicsItem(QtWidgets.QGraphicsItem):
    def __init__(self, width, height, offset, start, end):
        super().__init__()
        self.width = width
        self.height = height
        self.offset = offset
        self.start = start
        self.end = end
        self.init_rect()
        self.init_hour_texts()

    def boundingRect(self):
        return self.rect.boundingRect()

    def init_rect(self):
        self.rect = QtWidgets.QGraphicsRectItem(0, self.offset, self.width, self.height, parent=self)
        self.rect.setPen(QtGui.QColor(255,255,255))
        self.rect.setBrush(QtGui.QColor(255,255,255))

    def init_hour_texts(self):
        self.hours = []
        for i in range(self.start, self.end):
            hour = QtWidgets.QGraphicsSimpleTextItem(str(i), parent=self.rect)
            hour.setPos(0, (i-self.start)*self.height/(self.end-self.start) + self.offset)
            self.hours.append(hour)

    def paint(self, painter, option, widget):
        self.rect.paint(painter, option, widget)
                
