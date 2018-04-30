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
        self.new_customer_button.show()

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
        self.new_customer_button.hide()

    def init_reservation(self):
        self.service_buttons.check_services(self.reservation)
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
            text = "{0} Price: {1} Duration: {2}".format(service.name, service.price, service.duration)
            button = QtWidgets.QCheckBox(text)
            button.setToolTip(service.description)
            layout.addWidget(button, i + 1, 1)
            self.service_buttons.addButton(button, service.ID)
        for button in self.service_buttons.buttons():
            button.clicked.connect(self.update)
        self.price = QtWidgets.QDoubleSpinBox()
        value = self.service_buttons.get_price()
        self.price.setMaximum(max(1000000.0, value))
        self.price.setValue(value)
        self.price.setEnabled(False)
        layout.addWidget(QtWidgets.QLabel("Price"),len(services)+1,0)
        layout.addWidget(self.price,len(services)+1,1)
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
        if self.reservation:
            reservationID = self.reservation.ID
        else:
            reservationID = None
        self.resource_combo.clear()
        resources = self.database.get_resources()
        for resource in resources:
            if self.database.reservations.is_free(resource.ID, self.start.dateTime().toString("yyyy-MM-dd hh:mm"), self.end.dateTime().toString("yyyy-MM-dd hh:mm"),reservationID=reservationID):
                self.resource_combo.addItem(resource.name, resource)

    def create_customer_group_box(self):
        group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QHBoxLayout()
        self.create_new_customer_group_box()
        self.customer_combo = QtWidgets.QComboBox()
        customers = self.database.get_customers()
        for customer in customers:
            self.customer_combo.addItem(customer.name, customer)
        self.new_customer_button = QtWidgets.QCheckBox("New Customer")
        self.toggle_new_customer()
        self.new_customer_button.clicked.connect(self.toggle_new_customer)
        layout.addWidget(QtWidgets.QLabel('Customer'))
        layout.addWidget(self.customer_combo)
        layout.addWidget(self.new_customer_button)
        group_box.setLayout(layout)
        return group_box

    def toggle_new_customer(self):
        if self.new_customer_button.isChecked():
            self.new_customer_group_box.show()
            self.customer_combo.hide()
        else:
            self.new_customer_group_box.hide()
            self.customer_combo.show()

    def create_new_customer_group_box(self):
        self.new_customer_group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QFormLayout()
        self.name = QtWidgets.QLineEdit()
        self.email = QtWidgets.QLineEdit()
        layout.addRow(QtWidgets.QLabel('Name'), self.name)
        layout.addRow(QtWidgets.QLabel('Email'), self.email)
        self.new_customer_group_box.setLayout(layout)

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
        layout.addWidget(self.new_customer_group_box)
        layout.addWidget(self.create_service_group_box())
        layout.addWidget(self.create_date_time_group_box())
        layout.addWidget(self.create_resource_group_box())

        group_box.setLayout(layout)
        return group_box

    def update(self):
        self.end.setDateTime(self.start.dateTime().addSecs(self.service_buttons.get_duration()))
        value = self.service_buttons.get_price()
        self.price.setMaximum(max(1000000.0, value))
        self.price.setValue(value)
        self.add_free_resources()
        
    def accept(self):
        customer = self.customer_combo.currentData()
        resource = self.resource_combo.currentData()
        services = self.service_buttons.get_checked_services()
        start = self.start.dateTime()
        end = self.end.dateTime()
        if self.new_customer_button.isChecked():
            name = self.name.text()
            email = self.email.text()
            if name and email:
                customer = Customer(name=name, email=email)
            else:
                customer = None
        if not customer:
            self.error = MessageDialog('Please select a customer.')
            self.error.show()
        elif not resource:
            self.error = MessageDialog('Please select a resource. Change starting time to find a free resource.')
            self.error.show()
        elif not services:
            self.error = MessageDialog('Please select atleast one service.')
            self.error.show()
        else:
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
    def __init__(self, parent, resource=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.database = parent.database
        self.resource = resource
        layout = QtWidgets.QVBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.create_form_group_box()
        self.init_resource()
        layout.addWidget(self.form_group_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def init_resource(self):
        if self.resource:
            self.name.setText(self.resource.name)
            self.resource_type.setText(self.resource.resource_type)

    def create_form_group_box(self):
        self.form_group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QFormLayout()
        
        self.name = QtWidgets.QLineEdit()
        self.resource_type = QtWidgets.QLineEdit()

        layout.addRow(QtWidgets.QLabel('Name'), self.name)
        layout.addRow(QtWidgets.QLabel('Type (optional)'), self.resource_type)
        self.form_group_box.setLayout(layout)
        
    def accept(self):
        name = self.name.text()
        resource_type = self.resource_type.text()
        if name:
            if self.resource:
                resource = Resource(ID=self.resource.ID, name=name, resource_type=resource_type)
            else:
                resource = Resource(name=name, resource_type=resource_type)
            self.database.save(resource)
            self.information = MessageDialog("Resource added", icon=QtWidgets.QMessageBox.Information)
            self.information.show()
            self.close()
            self.parent.update()
        else:
            self.information = MessageDialog("Please fill in name.")
            self.information.show()

class ServiceDialog(QtWidgets.QDialog):
    def __init__(self, parent, service=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.service = service
        self.database = parent.database
        layout = QtWidgets.QVBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.create_form_group_box()
        self.init_service()
        layout.addWidget(self.form_group_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def init_service(self):
        if self.service:
            self.name.setText(self.service.name)
            self.price.setValue(self.service.price)
            self.duration.setValue(self.service.duration)
            self.description.setText(self.service.description)

    def create_form_group_box(self):
        self.form_group_box = QtWidgets.QGroupBox()
        layout = QtWidgets.QFormLayout()
        
        self.name = QtWidgets.QLineEdit()
        self.price = QtWidgets.QDoubleSpinBox()
        self.price.setMaximum(1000000)
        self.duration = QtWidgets.QDoubleSpinBox()
        self.duration.setRange(15, 1000000)
        self.description = QtWidgets.QTextEdit()

        layout.addRow(QtWidgets.QLabel('Name'), self.name)
        layout.addRow(QtWidgets.QLabel('Price'), self.price)
        layout.addRow(QtWidgets.QLabel('Duration (min)'), self.duration)
        layout.addRow(QtWidgets.QLabel('Description (optional)'), self.description)
        self.form_group_box.setLayout(layout)
        
    def accept(self):
        name = self.name.text()
        price = self.price.value()
        duration = self.duration.value()
        description = self.description.toPlainText()
        if name:
            if self.service:
                service = Service(ID=self.service.ID, name=name, price=price, duration=duration, description=description)
            else:
                service = Service(name=name, price=price, duration=duration, description=description)
            self.database.save(service)
            self.information = MessageDialog("Service added", icon=QtWidgets.QMessageBox.Information)
            self.information.show()
            self.close()
            self.parent.update()
        else:
            self.information = MessageDialog("Please fill in name.")
            self.information.show()


class CustomerDialog(QtWidgets.QDialog):
    def __init__(self, parent, customer=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.database = parent.database
        self.customer = customer
        layout = QtWidgets.QVBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.create_form_group_box()
        self.init_customer()
        layout.addWidget(self.form_group_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def init_customer(self):
        if self.customer:
            self.name.setText(self.customer.name)
            self.email.setText(self.customer.email)

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
        if name and email:
            if self.customer:
                customer = Customer(ID=self.customer.ID, name=name, email=email)
            else:
                customer = Customer(name=name, email=email)
            self.database.save(customer)
            self.information = MessageDialog("Customer added", icon=QtWidgets.QMessageBox.Information)
            self.information.show()
            self.close()
            self.parent.update()
        else:
            self.information = MessageDialog("Please fill in name and email.")
            self.information.show()

class ResourceManageDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.database = parent.database
        self.layout = QtWidgets.QVBoxLayout()

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        delete_button = QtWidgets.QPushButton("Delete")
        edit_button = QtWidgets.QPushButton("Edit")
        add_button = QtWidgets.QPushButton("New")
        buttonBox.addButton(delete_button, 2)
        buttonBox.addButton(edit_button, 3)
        buttonBox.addButton(add_button, 3)
        delete_button.clicked.connect(self.delete)
        edit_button.clicked.connect(self.edit)
        add_button.clicked.connect(self.add)

        self.create_list_widget()
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(buttonBox)
        self.setLayout(self.layout)

    def create_list_widget(self):
        self.listWidget = QtWidgets.QListWidget()
        for resource in self.database.get_resources():
            item = QtWidgets.QListWidgetItem(resource.name)
            item.setData(QtCore.Qt.UserRole, resource)
            self.listWidget.addItem(item)

    def edit(self):
        item = self.listWidget.currentItem()
        if item:
            resource = item.data(QtCore.Qt.UserRole)
            self.resourceDialog = ResourceDialog(self.parent, resource=resource)
            self.resourceDialog.show()
            self.close()

    def delete(self):
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        if item:
            resource = item.data(QtCore.Qt.UserRole)
            self.database.delete(resource)
            item = None
            self.information = MessageDialog("Resource and all related reservations deleted.", icon=QtWidgets.QMessageBox.Information)
            self.information.show()
            self.parent.update()

    def add(self):
        self.resourceDialog = ResourceDialog(self.parent)
        self.resourceDialog.show()
        self.close()

class ServiceManageDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.database = parent.database
        self.layout = QtWidgets.QVBoxLayout()

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        delete_button = QtWidgets.QPushButton("Delete")
        edit_button = QtWidgets.QPushButton("Edit")
        add_button = QtWidgets.QPushButton("New")
        buttonBox.addButton(delete_button, 2)
        buttonBox.addButton(edit_button, 3)
        buttonBox.addButton(add_button, 3)
        delete_button.clicked.connect(self.delete)
        edit_button.clicked.connect(self.edit)
        add_button.clicked.connect(self.add)

        self.create_list_widget()
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(buttonBox)
        self.setLayout(self.layout)

    def create_list_widget(self):
        self.listWidget = QtWidgets.QListWidget()
        for service in self.database.get_services():
            item = QtWidgets.QListWidgetItem(service.name)
            item.setData(QtCore.Qt.UserRole, service)
            self.listWidget.addItem(item)

    def edit(self):
        item = self.listWidget.currentItem()
        if item:
            service = item.data(QtCore.Qt.UserRole)
            self.serviceDialog = ServiceDialog(self.parent, service=service)
            self.serviceDialog.show()
            self.close()

    def delete(self):
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        if item:
            service = item.data(QtCore.Qt.UserRole)
            self.database.delete(service)
            item = None
            self.information = MessageDialog("Service deleted and removed from all related reservations.", icon=QtWidgets.QMessageBox.Information)
            self.information.show()
            self.parent.update()

    def add(self):
        self.serviceDialog = ServiceDialog(self.parent)
        self.serviceDialog.show()
        self.close()

class CustomerManageDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.database = parent.database
        self.layout = QtWidgets.QVBoxLayout()

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        delete_button = QtWidgets.QPushButton("Delete")
        edit_button = QtWidgets.QPushButton("Edit")
        add_button = QtWidgets.QPushButton("New")
        buttonBox.addButton(delete_button, 2)
        buttonBox.addButton(edit_button, 3)
        buttonBox.addButton(add_button, 3)
        delete_button.clicked.connect(self.delete)
        edit_button.clicked.connect(self.edit)
        add_button.clicked.connect(self.add)

        self.create_list_widget()
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(buttonBox)
        self.setLayout(self.layout)

    def create_list_widget(self):
        self.listWidget = QtWidgets.QListWidget()
        for customer in self.database.get_customers():
            item = QtWidgets.QListWidgetItem(customer.name)
            item.setData(QtCore.Qt.UserRole, customer)
            self.listWidget.addItem(item)

    def edit(self):
        item = self.listWidget.currentItem()
        if item:
            customer = item.data(QtCore.Qt.UserRole)
            self.customerDialog = CustomerDialog(self.parent, customer=customer)
            self.customerDialog.show()
            self.close()

    def delete(self):
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        if item:
            customer = item.data(QtCore.Qt.UserRole)
            self.database.delete(customer)
            item = None
            self.information = MessageDialog("Customer and all related reservations deleted.", icon=QtWidgets.QMessageBox.Information)
            self.information.show()
            self.parent.update()

    def add(self):
        self.customerDialog = CustomerDialog(self.parent)
        self.customerDialog.show()
        self.close()

class MessageDialog(QtWidgets.QMessageBox):
    def __init__(self, text, icon=QtWidgets.QMessageBox.Warning):
        super().__init__()
        self.setIcon(icon)
        self.setText(text)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)

    def accept(self):
        self.parent.activateWindow()
        super().accept()

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

