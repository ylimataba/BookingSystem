from PyQt5 import QtWidgets, QtCore, QtGui
from models import Reservation, Resource

class ReservationGraphicsItem(QtWidgets.QGraphicsItem):
    def __init__(self, reservation, width, height, offset):
        super().__init__()
        self.width = width
        self.height = height
        self.offset = offset
        self.reservation = reservation
        self.x = self.reservation.resource.ID - 1
        self.y = (self.reservation.start.time().hour() * 3600 + self.reservation.start.time().minute() * 60) / 3600
        self.duration = self.reservation.start.secsTo(self.reservation.end) / 3600
        self.init_rect()
        self.init_text()

    def boundingRect(self):
        return self.rect.boundingRect()

    def init_rect(self):
        self.rect = QtWidgets.QGraphicsRectItem(self.x*self.width + self.offset, self.y*self.height, self.width, self.duration*self.height, parent=self)
        self.rect.setBrush(QtGui.QColor(230,230,230))

    def init_text(self):
        self.text = QtWidgets.QGraphicsTextItem(parent=self.rect)
        self.text.setHtml(self.reservation.to_html())
        self.text.setPos(self.x*self.width + self.offset, self.y*self.height)

    def paint(self, painter, option, widget):
        self.rect.paint(painter, option, widget)
        self.text.paint(painter, option, widget)
                
