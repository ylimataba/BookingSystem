from PyQt5 import QtWidgets, QtCore, QtGui
from models import Reservation, Resource, Service, Customer
from hour_row_graphics_item import HourRowGraphicsItem
from column_header_graphics_item import ColumnHeaderGraphicsItem

class ReservationDialog(QtWidgets.QDialog):
    def __init__(self, parent, reservation=None):
        super().__init__(parent=parent)
        self.reservation = reservation
        self.database = parent.database
        layout = QtWidgets.QVBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.create_reservation_group_box())
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        self.start.dateTimeChanged.connect(self.update)

    def create_service_group_box(self):
        group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel('Services'),0,0)
        services = self.database.get_services()
        self.service_buttons = ServiceButtonGroup(self.database)
        self.service_buttons.setExclusive(False)
        for i, service in enumerate(services):
            button = QtWidgets.QCheckBox(service.name)
            button.setToolTip(service.description)
            layout.addWidget(button, i + 1, 1)
            self.service_buttons.addButton(button, service.ID)
        for button in self.service_buttons.buttons():
            button.clicked.connect(self.update)
        group_box.setLayout(layout)
        return group_box

    def create_resource_group_box(self):
        group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QHBoxLayout()
        resources = self.database.get_resources()
        self.resource_combo = QtWidgets.QComboBox()
        for resource in resources:
            self.resource_combo.addItem(resource.name, resource)
        layout.addWidget(QtWidgets.QLabel('Resource'))
        layout.addWidget(self.resource_combo)
        if self.reservation:
            self.resource_combo.setCurrentIndex(self.resource_combo.findData(self.reservation.resource))
        group_box.setLayout(layout)
        return group_box

    def create_customer_group_box(self):
        group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QHBoxLayout()
        customers = self.database.get_customers()
        self.customer_combo = QtWidgets.QComboBox()
        for customer in customers:
            self.customer_combo.addItem(customer.name, customer)
        layout.addWidget(QtWidgets.QLabel('Customer'))
        layout.addWidget(self.customer_combo)
        if self.reservation:
            self.customer_combo.setCurrentIndex(self.customer_combo.findData(self.reservation.customer))
        group_box.setLayout(layout)
        return group_box

    def create_date_time_group_box(self):
        group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QGridLayout()
        self.start = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.end = QtWidgets.QDateTimeEdit(self.start.dateTime().addSecs(self.service_buttons.get_duration()))
        self.start.setDisplayFormat("d.M.yyyy HH:mm")
        self.end.setDisplayFormat("d.M.yyyy HH:mm")
        self.start.setCalendarPopup(True)
        self.end.setEnabled(False)
        self.start.dateTimeChanged.connect(self.update)
        if self.reservation:
            self.start.setDateTime(self.reservation.start)
            self.end.setDateTime(self.reservation.end)
        else:
            self.start.setMinimumDateTime(self.start.dateTime())
        layout.addWidget(QtWidgets.QLabel('Start date & time'),0,0)
        layout.addWidget(self.start,0,1)
        layout.addWidget(QtWidgets.QLabel('End date & time'),1,0)
        layout.addWidget(self.end,1,1)
        group_box.setLayout(layout)
        return group_box

    def create_reservation_group_box(self):
        group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.create_customer_group_box())
        layout.addWidget(self.create_resource_group_box())
        layout.addWidget(self.create_service_group_box())
        layout.addWidget(self.create_date_time_group_box())

        group_box.setLayout(layout)
        return group_box

    def update(self):
        self.end.setDateTime(self.start.dateTime().addSecs(self.service_buttons.get_duration()))
        
    def accept(self):
        customer = self.customer_combo.currentData()
        resource = self.resource_combo.currentData()
        services = self.service_buttons.get_checked_services()
        start = self.start.dateTime()
        end = self.end.dateTime()
        if self.reservation:
            reservation = Reservation(ID=self.reservation.ID, customer=customer, services=services, resource=resource, start=start, end=end)
        else:
            reservation = Reservation(services=services, customer=customer, resource=resource, start=start, end=end)
        if not self.database.save(reservation):
            self.error = ErrorMessageDialog('Failed to create reservation')
            self.error.show()
        self.close()

class ResourceDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
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

class ServiceDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
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
        self.price = QtWidgets.QLineEdit()
        self.duration = QtWidgets.QLineEdit()
        self.description = QtWidgets.QTextEdit()

        layout.addRow(QtWidgets.QLabel('Name'), self.name)
        layout.addRow(QtWidgets.QLabel('Price'), self.price)
        layout.addRow(QtWidgets.QLabel('Duration'), self.duration)
        layout.addRow(QtWidgets.QLabel('Description'), self.description)
        self.form_group_box.setLayout(layout)
        
    def accept(self):
        name = self.name.text()
        price = float(self.price.text())
        duration = float(self.duration.text())
        description = self.description.toPlainText()
        service = Service(name=name, price=price, duration=duration, description=description)
        self.database.save(service)
        self.close()

class CustomerDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
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
        self.email = QtWidgets.QLineEdit()

        layout.addRow(QtWidgets.QLabel('Name'), self.name)
        layout.addRow(QtWidgets.QLabel('Email'), self.email)
        self.form_group_box.setLayout(layout)
        
    def accept(self):
        name = self.name.text()
        email = self.email.text()
        customer = Customer(name=name, email=email)
        self.database.save(customer)
        self.close()


class ErrorMessageDialog(QtWidgets.QMessageBox):
    def __init__(self, text):
        super().__init__()
        self.setIcon(QtWidgets.QMessageBox.Warning)
        self.setText(text)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)

class ServiceButtonGroup(QtWidgets.QButtonGroup):
    def __init__(self, database):
        super().__init__()
        self.database = database

    def get_checked_services(self):
        services = []
        for button in self.buttons():
            if button.isChecked():
                service = self.database.get_services(ID=self.id(button))
                services.append(service)
        return services

    def get_duration(self):
        duration = 0
        services = self.get_checked_services()
        for service in services:
            duration += service.duration * 60
        return duration

