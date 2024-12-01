from PyQt6.QtCore import QObject, pyqtSignal
from MySQLdb import Error
from models.customer_model import Customer
from database import create_connection

class CustomerController:
    def __init__(self, conn=None):
        if conn:
            self.conn = conn
        else:
            self.conn = create_connection()

    def create_customer(self, name, phone):
        try:
            cursor = self.conn.cursor()
            sql = ''' INSERT INTO customer(name, phone)
                      VALUES(%s, %s)'''
            cursor.execute(sql, (name, phone))
            self.conn.commit()
            return Customer(cursor.lastrowid, name, phone)
        except Error as e:
            print(f"Lỗi: '{e}'")
            return None

    def get_customer_by_id(self, customer_id):
        try:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM customer WHERE id = %s"
            cursor.execute(sql, (customer_id,))
            row = cursor.fetchone()
            if row:
                return Customer(*row)
            return None
        except Error as e:
            print(f"Lỗi: '{e}'")
            return None

    def get_customer_by_name_phone(self, name, phone):
        try:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM customer WHERE name = %s AND phone = %s"
            cursor.execute(sql, (name, phone))
            row = cursor.fetchone()
            if row:
                return Customer(*row)
            return None
        except Error as e:
            print(f"Lỗi: '{e}'")
            return None

    def get_customer(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM customer")
            rows = cursor.fetchall()
            return [Customer(*row) for row in rows]
        except Error as e:
            print(f"Lỗi: '{e}'")
            return []


    def update_customer(self, id, name, phone):
        try:
            cursor = self.conn.cursor()
            sql = '''UPDATE customer SET name = %s, phone = %s WHERE id = %s'''
            cursor.execute(sql, (name, phone, id))
            self.conn.commit()
        except Error as e:
            print(f"Lỗi: '{e}'")

    def delete_customer(self, id):
        try:
            cursor = self.conn.cursor()
            sql = 'DELETE FROM customer WHERE id = %s'
            cursor.execute(sql, (id,))
            self.conn.commit()
        except Error as e:
            print(f"Lỗi: '{e}'")
