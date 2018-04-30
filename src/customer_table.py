from table import Table
from models import Customer

class CustomerTable(Table):
    def __init__(self, connection):
        super().__init__(connection)
        self.cursor.execute('CREATE TABLE IF NOT EXISTS customers (customerID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)')
        self.connection.commit()
        
    def save(self, customer):
        if customer.ID:
            self.cursor.execute('UPDATE customers SET name=?, email=? WHERE customerID=?', customer.get_data())
            self.connection.commit()
        else:
            self.cursor.execute('INSERT INTO customers(name, email) VALUES (?,?)', customer.get_data())
            self.connection.commit()
            customer.ID = self.cursor.lastrowid
        return True

    def get_all(self):
        customers = []
        self.cursor.execute('SELECT * FROM customers ORDER BY name COLLATE NOCASE')
        rows = self.cursor.fetchall()
        for row in rows:
            customers.append(Customer(row=row))
        return customers

    def get_by_id(self, ID):
        self.cursor.execute('SELECT * FROM customers WHERE customerID=?', (ID,))
        customer = Customer(row=self.cursor.fetchone())
        return customer

    def delete(self, customer):
        self.cursor.execute('DELETE FROM customers WHERE customerID=?', (customer.ID,))
        self.connection.commit()

    def reset(self):
        self.cursor.execute('DROP TABLE IF EXISTS customers')
        self.connection.commit()
        self = CustomerTable(self.connection)

