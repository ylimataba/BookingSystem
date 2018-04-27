from PyQt5 import QtWidgets, QtCore, QtGui
from models import Reservation, Resource
from reservation_graphics_item import ReservationGraphicsItem
from hour_row_graphics_item import HourRowGraphicsItem
from column_header_graphics_item import ColumnHeaderGraphicsItem
from dialogs import ReservationDialog, ResourceDialog

class GUI(QtWidgets.QMainWindow):
    '''
    The class GUI handles the drawing of a RobotWorld and allows user to
    interact with it.
    '''
    def __init__(self, database):
        super().__init__()
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.database = database
        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout() # Horizontal main layout
        self.centralWidget().setLayout(self.horizontal)
        self.init_window()
        self.init_buttons()
        self.add_reservation_view()

    def init_buttons(self):
        '''
        Adds buttons to the window and connects them to their respective functions
        See: QPushButton at http://doc.qt.io/qt-5/qpushbutton.html
        '''
        self.buttons = QtWidgets.QGroupBox()
        layout = QtWidgets.QVBoxLayout()
        self.buttons.setLayout(layout)

        self.reservation = QtWidgets.QPushButton("Add reservation")
        self.reservation.clicked.connect(self.add_reservation)
        layout.addWidget(self.reservation)

        self.resource = QtWidgets.QPushButton("Add resource")
        self.resource.clicked.connect(self.add_resource)
        layout.addWidget(self.resource)

        #self.calendar = QtWidgets.QCalendarWidget()
        self.calendar = MyCalendar(self.database)
        self.calendar.setMaximumWidth(self.screen.width() * 0.2)
        self.calendar.selectionChanged.connect(self.add_reservation_view)
        layout.addWidget(self.calendar)

        layout.setAlignment(QtCore.Qt.AlignTop)

        self.horizontal.addWidget(self.buttons)

    def init_window(self):
        '''
        Sets up the window.
        '''
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        #self.setGeometry(screen)
        self.setWindowTitle('Varausjärjestelmä')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        #self.scene.setSceneRect(0, 0, 0.8*screen.width(), 1.5*screen.height())

        # Add a view for showing the scene
        #self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view = MyView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)

    def draw_hour_lines(self, width, height, offset, number_of_lines):
        for i in range(number_of_lines):
            line = QtWidgets.QGraphicsLineItem(0, i*height+offset, width, i*height+offset)
            self.scene.addItem(line)

    def add_reservation_view(self):
        self.scene.clear()
        date = self.calendar.selectedDate()
        reservations = self.database.get_reservations(date=date)
        if reservations:
            (start, end) = self.database.get_start_and_end(date)
            number_of_lines = end - start
            resources = self.database.resources.get_all()
            offset = 30
            width = (self.screen.width() - offset) / min(5, max(len(resources),1))
            height = self.screen.height() / 12
            hours = HourRowGraphicsItem(offset-15, height * number_of_lines, offset, start, end)
            headers = ColumnHeaderGraphicsItem(self.screen.width(), offset-5, resources, offset)
            self.draw_hour_lines(self.screen.width(), height, offset, number_of_lines)
            for reservation in reservations:
                item = ReservationGraphicsItem(self.database, reservation, width, height, offset, date, start)
                self.scene.addItem(item)
            self.scene.addItem(hours)
            self.scene.addItem(headers)
        else:
            text = QtWidgets.QGraphicsSimpleTextItem("No reservations for selected date")
            self.scene.addItem(text)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

    def add_reservation(self, reservation=None):
        self.reservation_dialog = ReservationDialog(self, reservation=reservation)
        self.reservation_dialog.show()

    def add_resource(self):
        self.resource_dialog = ResourceDialog()
        self.resource_dialog.show()

class MyView(QtWidgets.QGraphicsView):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)
        self.scene = scene
        self.setMinimumWidth(0.5*parent.screen.width())
   
    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        for item in self.scene.items():
            scenePos = self.mapToScene(0, 0)
            if isinstance(item, HourRowGraphicsItem):
                item.setPos(scenePos.x(), item.y())
            elif isinstance(item, ColumnHeaderGraphicsItem):
                item.setPos(item.x(), scenePos.y())

class MyCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, database):
        super().__init__()
        self.database = database

    def paintCell(self, painter, rect, date):
        reservations = self.database.get_reservations(date=date)
        if reservations and self.selectedDate() != date:
            painter.save()
            painter.setPen(QtCore.Qt.white)
            painter.setBrush(QtGui.QColor(152, 251, 152))
            painter.drawRect(rect)
            if date.dayOfWeek() > 5:
                painter.setPen(QtCore.Qt.red)
            else:
                painter.setPen(QtCore.Qt.black)
            painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
            painter.restore()
        else:
            super().paintCell(painter, rect, date)
