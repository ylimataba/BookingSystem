from PyQt5 import QtWidgets, QtCore, QtGui
from models import Reservation, Resource
from hour_row_graphics_item import HourRowGraphicsItem
from column_header_graphics_item import ColumnHeaderGraphicsItem

class ReservationDialog(QtWidgets.QDialog):
    def __init__(self, database, reservation=None):
        super().__init__()
        self.reservation = reservation
        self.database = database
        layout = QtWidgets.QVBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.create_form_group_box()
        layout.addWidget(self.form_group_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        self.start.dateTimeChanged.connect(self.update)

    def create_form_group_box(self):
        self.form_group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QFormLayout()
        self.start = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.end = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime().addSecs(3600))
        self.start.setDisplayFormat("d.M.yyyy HH:mm")
        self.end.setDisplayFormat("d.M.yyyy HH:mm")
        self.start.setCalendarPopup(True)
        self.end.setCalendarPopup(True)
        self.start.setMinimumDateTime(self.start.dateTime())
        self.end.setMinimumDateTime(self.start.dateTime().addSecs(60))

        self.resources = self.database.resources.get_all()
        self.combo = QtWidgets.QComboBox()
        for resource in self.resources:
            self.combo.addItem(resource.name)

        if self.reservation:
            self.start.setDateTime(self.reservation.start)
            self.end.setDateTime(self.reservation.end)
            self.combo.setCurrentIndex(self.resources.index(self.reservation.resource))
        layout.addRow(QtWidgets.QLabel('Resource'), self.combo)
        layout.addRow(QtWidgets.QLabel('Start date & time'), self.start)
        layout.addRow(QtWidgets.QLabel('End date & time'), self.end)
        self.form_group_box.setLayout(layout)

    def update(self):
        self.end.setMinimumDateTime(self.start.dateTime().addSecs(60))
        if self.end.dateTime() < self.end.minimumDateTime():
            self.end.setDateTime(self.end.minimumDateTime())

        
    def accept(self):
        resource = next(x for x in self.resources if x.name==self.combo.currentText())
        start = self.start.dateTime()
        end = self.end.dateTime()
        if self.reservation:
            reservation = Reservation(ID=self.reservation.ID, resource=resource, start=start, end=end)
        else:
            reservation = Reservation(resource=resource, start=start, end=end)
        if not self.database.save(reservation):
            self.error = ErrorMessageDialog('Failed to create reservation')
            self.error.show()
            print('error')
        self.close()

class ResourceDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
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

class ErrorMessageDialog(QtWidgets.QMessageBox):
    def __init__(self, text):
        super().__init__()
        self.setIcon(QtWidgets.QMessageBox.Warning)
        self.setText(text)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
