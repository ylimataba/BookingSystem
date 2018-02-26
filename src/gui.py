from PyQt5 import QtWidgets, QtCore, QtGui

class GUI(QtWidgets.QMainWindow):
    '''
    The class GUI handles the drawing of a RobotWorld and allows user to
    interact with it.
    '''
    def __init__(self):
        super().__init__()
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
        #self.next_turn_btn.clicked.connect(self.world.next_full_turn)
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
