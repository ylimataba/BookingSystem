from PyQt5 import QtWidgets, QtCore, QtGui
from reservation import Reservation

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

        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.update_robots)
        self.timer.start(10) # Milliseconds

    def init_buttons(self):
        '''
        Adds buttons to the window and connects them to their respective functions
        See: QPushButton at http://doc.qt.io/qt-5/qpushbutton.html
        '''
        self.buttons = QtWidgets.QGroupBox()
        layout = QtWidgets.QVBoxLayout()
        self.buttons.setLayout(layout)

        self.reservation = QtWidgets.QPushButton("Uusi varaus")
        self.dialog = AddReservationGUI(self)
        self.reservation.clicked.connect(self.dialog.show)
        layout.addWidget(self.reservation)

        self.service = QtWidgets.QPushButton("Muokkaa palveluja")
        #self.next_turn_btn.clicked.connect(self.world.next_full_turn)
        layout.addWidget(self.service)

        self.resource = QtWidgets.QPushButton("Muokkaa resursseja")
        #self.next_turn_btn.clicked.connect(self.world.next_full_turn)
        layout.addWidget(self.resource)

        self.see_reservations = QtWidgets.QPushButton("Katsele varauksia")
        #self.next_turn_btn.clicked.connect(self.world.next_full_turn)
        layout.addWidget(self.see_reservations)

        layout.setAlignment(QtCore.Qt.AlignTop)

        self.horizontal.addWidget(self.buttons)

    def init_window(self):
        '''
        Sets up the window.
        '''
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Varausjärjestelmä')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 700)

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)

class AddReservationGUI(QtWidgets.QDialog):
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

        layout.addRow(QtWidgets.QLabel('Reservation date'), self.dateEdit);
        layout.addRow(QtWidgets.QLabel('Start time'), self.start)
        layout.addRow(QtWidgets.QLabel('End time'), self.end)
        self.form_group_box.setLayout(layout);
        
    def accept(self):
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        start = self.start.time().toString("hh.mm")
        end = self.end.time().toString("hh.mm")
        reservation = Reservation(date=date, start=start, end=end)
        reservation.save(self.database.reservations)
        self.close()
