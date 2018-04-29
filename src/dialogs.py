from PyQt5 import QtWidgets, QtCore, QtGui
from models import Reservation, Resource, Service, Customer
from hour_row_graphics_item import HourRowGraphicsItem
from column_header_graphics_item import ColumnHeaderGraphicsItem

class ReservationDialog(QtWidgets.QDialog):
    def __init__(self, parent, reservation=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.reservation = reservation
        self.database = parent.database
        layout = QtWidgets.QVBoxLayout()
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.create_reservation_group_box())
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.start.dateTimeChanged.connect(self.update)
        if self.reservation:
            self.edit_off()
            self.init_reservation()

    def edit(self):
        self.buttonBox.removeButton(self.edit_button)
        self.service_buttons.setEnabled(True)
        self.resource_combo.setEnabled(True)
        self.customer_combo.setEnabled(True)
        self.start.setEnabled(True)

    def delete(self):
        self.database.delete(self.reservation)
        self.information = MessageDialog("Resevation deleted", icon=QtWidgets.QMessageBox.Information)
        self.information.show()
        self.close()
        self.parent.update()

    def edit_off(self):
        self.delete_button = QtWidgets.QPushButton("Delete")
        self.edit_button = QtWidgets.QPushButton("Edit")
        self.buttonBox.addButton(self.delete_button, 2)
        self.buttonBox.addButton(self.edit_button, 3)
        self.delete_button.clicked.connect(self.delete)
        self.edit_button.clicked.connect(self.edit)
        self.service_buttons.setEnabled(False)
        self.resource_combo.setEnabled(False)
        self.customer_combo.setEnabled(False)
        self.start.setEnabled(False)

    def init_reservation(self):
        self.service_buttons.check_services(self.reservation)
        self.resource_combo.addItem(self.reservation.resource.name, self.reservation.resource)
        self.resource_combo.setCurrentIndex(self.resource_combo.findText(self.reservation.resource.name))
        self.customer_combo.setCurrentIndex(self.customer_combo.findText(self.reservation.customer.name))
        self.start.setDateTime(self.reservation.start)
        self.end.setDateTime(self.reservation.end)

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
        self.price = QtWidgets.QLineEdit(str(self.service_buttons.get_price()))
        self.price.setEnabled(False)
        layout.addWidget(QtWidgets.QLabel("Price"),i+2,0)
        layout.addWidget(self.price,i+2,1)
        group_box.setLayout(layout)
        return group_box

    def create_resource_group_box(self):
        group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QHBoxLayout()
        self.resource_combo = QtWidgets.QComboBox()
        self.add_free_resources()
        layout.addWidget(QtWidgets.QLabel('Resource'))
        layout.addWidget(self.resource_combo)
        group_box.setLayout(layout)
        return group_box

    def add_free_resources(self):
        self.resource_combo.clear()
        resources = self.database.get_resources()
        for resource in resources:
            if self.database.resources.is_free(resource.ID, self.start.dateTime().toString("yyyy-MM-dd hh:mm"), self.end.dateTime().toString("yyyy-MM-dd hh:mm")):
                self.resource_combo.addItem(resource.name, resource)

    def create_customer_group_box(self):
        group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QHBoxLayout()
        customers = self.database.get_customers()
        self.customer_combo = QtWidgets.QComboBox()
        for customer in customers:
            self.customer_combo.addItem(customer.name, customer)
        layout.addWidget(QtWidgets.QLabel('Customer'))
        layout.addWidget(self.customer_combo)
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
        layout.addWidget(self.create_service_group_box())
        layout.addWidget(self.create_date_time_group_box())
        layout.addWidget(self.create_resource_group_box())

        group_box.setLayout(layout)
        return group_box

    def update(self):
        self.end.setDateTime(self.start.dateTime().addSecs(self.service_buttons.get_duration()))
        self.price.setText(str(self.service_buttons.get_price()))
        self.add_free_resources()
        
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
            self.error = MessageDialog('Failed to create reservation')
            self.error.show()
        else:
            self.information = MessageDialog("Resevation added", icon=QtWidgets.QMessageBox.Information)
            self.information.show()
        self.close()
        self.parent.update()

class ResourceDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
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
        self.information = MessageDialog("Resource added", icon=QtWidgets.QMessageBox.Information)
        self.information.show()
        self.close()
        self.parent.update()

class ServiceDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
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
        self.information = MessageDialog("Service added", icon=QtWidgets.QMessageBox.Information)
        self.information.show()
        self.close()
        self.parent.update()

class CustomerDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
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
        self.information = MessageDialog("Customer added", icon=QtWidgets.QMessageBox.Information)
        self.information.show()
        self.close()
        self.parent.update()


class MessageDialog(QtWidgets.QMessageBox):
    def __init__(self, text, icon=QtWidgets.QMessageBox.Warning):
        super().__init__()
        self.setIcon(icon)
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

    def get_price(self):
        price = 0
        services = self.get_checked_services()
        for service in services:
            price += service.price
        return price

    def check_services(self, reservation):
        for service in reservation.services:
            self.button(service.ID).setChecked(True)

    def setEnabled(self, value):
        for button in self.buttons():
            button.setEnabled(value)

