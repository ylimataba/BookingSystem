from PyQt5 import QtWidgets, QtCore, QtGui
from models import Reservation, Resource

class GUI(QtWidgets.QMainWindow):
    '''
    The class GUI handles the drawing of a RobotWorld and allows user to
    interact with it.
    '''
    def __init__(self, database):
        super().__init__()
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

        layout.setAlignment(QtCore.Qt.AlignTop)

        self.horizontal.addWidget(self.buttons)

    def init_window(self):
        '''
        Sets up the window.
        '''
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        self.setWindowTitle('Varausjärjestelmä')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        #self.scene.setSceneRect(0, 0, 700, 700)

        # Add a view for showing the scene
        #self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view = MyView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)

        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar.selectionChanged.connect(self.add_reservation_view)
        self.horizontal.addWidget(self.calendar)

    def add_reservation_view(self):
        i = 0
        reservations = self.database.get_reservations(date=self.calendar.selectedDate().toString('yyyy-MM-dd'))
        resources = self.database.resources.get_all()
        self.scene.clear()
        width = self.view.width() / max(len(resources),1)
        height = self.view.height() / max(len(reservations),1)
        for reservation in reservations:
            #rect = QtWidgets.QGraphicsRectItem(width*i,0,width,height)
            text = QtWidgets.QGraphicsTextItem()
            text.setHtml(reservation.to_html())
            text.setPos(0,i*height)
            self.scene.addItem(text)
            i += 1
        #self.view.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def add_reservation(self):
        self.reservation_dialog = AddReservation(self)
        self.reservation_dialog.show()

    def add_resource(self):
        self.resource_dialog = AddResource(self)
        self.resource_dialog.show()

class AddReservation(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.database = parent.database
        layout = QtWidgets.QVBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.create_form_group_box()
        layout.addWidget(self.form_group_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def create_form_group_box(self):
        self.form_group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QFormLayout()
        self.dateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.dateEdit.setDisplayFormat("d.M.yyyy");
        self.dateEdit.setCalendarPopup(True)

        self.start = QtWidgets.QTimeEdit(QtCore.QTime.currentTime())
        self.end = QtWidgets.QTimeEdit(QtCore.QTime.currentTime().addSecs(3600))
        self.start.setDisplayFormat("HH:mm")
        self.end.setDisplayFormat("HH:mm")

        self.resources = self.database.resources.get_all()
        self.combo = QtWidgets.QComboBox()
        for resource in self.resources:
            self.combo.addItem(resource.name)

        layout.addRow(QtWidgets.QLabel('Resource'), self.combo)
        layout.addRow(QtWidgets.QLabel('Reservation date'), self.dateEdit)
        layout.addRow(QtWidgets.QLabel('Start time'), self.start)
        layout.addRow(QtWidgets.QLabel('End time'), self.end)
        self.form_group_box.setLayout(layout)
        
    def accept(self):
        resource = next(x for x in self.resources if x.name==self.combo.currentText())
        date = self.dateEdit.date()
        start = QtCore.QDateTime(date, self.start.time())
        end = QtCore.QDateTime(date, self.end.time())
        reservation = self.database.new_reservation(resource=resource, start=start, end=end)
        if not reservation:
            print('Failed to create reservation')
        self.close()

class AddResource(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.database = parent.database
        layout = QtWidgets.QVBoxLayout()

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.create_form_group_box()

        layout.addWidget(self.form_group_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def create_form_group_box(self):
        self.form_group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QFormLayout()
        
        self.name = QtWidgets.QLineEdit()
        self.resource_type = QtWidgets.QLineEdit()

        layout.addRow(QtWidgets.QLabel('Name'), self.name)
        layout.addRow(QtWidgets.QLabel('Type'), self.resource_type)
        self.form_group_box.setLayout(layout)
        
    def accept(self):
        name = self.name.text()
        resource_type = self.resource_type.text()
        resource = Resource(name=name, resource_type=resource_type)
        self.database.save(resource)
        self.close()


class MyView(QtWidgets.QGraphicsView):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)
        self.scene = scene
        #self.setMinimumHeight(500)
        #self.setMinimumWidth(500)
    
    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)

