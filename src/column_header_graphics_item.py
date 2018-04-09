from PyQt5 import QtWidgets, QtCore, QtGui
from models import Reservation, Resource

class ColumnHeaderGraphicsItem(QtWidgets.QGraphicsItem):
    def __init__(self, width, height, resources, offset):
        super().__init__()
        self.width = width
        self.height = height
        self.resources = resources
        self.offset = offset
        self.header_width = self.width / len(resources)
        self.init_rect()
        self.init_headers()

    def boundingRect(self):
        return self.rect.boundingRect()

    def init_rect(self):
        self.rect = QtWidgets.QGraphicsRectItem(self.offset, 0, self.width, self.height, parent=self)
        self.rect.setPen(QtGui.QColor(255,255,255))
        self.rect.setBrush(QtGui.QColor(240,240,240))

    def init_headers(self):
        self.headers = []
        for i in range(len(self.resources)):
            header = QtWidgets.QGraphicsSimpleTextItem(self.resources[i].name, parent=self.rect)
            header.setPos(i*self.header_width + self.offset, 0)
            self.headers.append(header)

    def paint(self, painter, option, widget):
        self.rect.paint(painter, option, widget)
