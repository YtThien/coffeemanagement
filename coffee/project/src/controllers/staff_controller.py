from MySQLdb import Error
from models.staff_model import Staff
from database import create_connection

class StaffController:
    def __init__(self, conn=None):
        if conn is None:
            self.conn = create_connection()
        else:
            self.conn = conn
    def create_staff(self, name_staff, phone, email, position, username, password, id_role):
        try:
            cursor = self.conn.cursor()
            sql = '''INSERT INTO staff(name, phone, email, position, username, password, id_role)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (name_staff, phone, email, position, username, password, id_role))
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Lỗi create: '{e}'")

    def get_staff(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM staff")
            rows = cursor.fetchall()
            return [Staff(*row) for row in rows]
        except Error as e:
            print(f"Lỗi get_staff: '{e}'")

    def update_staff(self, id, name_staff, phone, email, position, username, password, id_role):
        try:
            cursor = self.conn.cursor()
            sql = '''UPDATE staff SET name = %s, phone = %s, email = %s, position = %s, 
                     username = %s, password = %s, id_role = %s WHERE id = %s'''
            cursor.execute(sql, (name_staff, phone, email, position, username, password, id_role, id))
            self.conn.commit()
        except Error as e:
            print(f"Lỗi update: '{e}'")

    def delete_staff(self, id):
        try:
            cursor = self.conn.cursor()
            sql = 'DELETE FROM staff WHERE id = %s'
            cursor.execute(sql, (id,))
            self.conn.commit()
        except Error as e:
            print(f"Lỗi delete: '{e}'")

    def get_role(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT role_id, role_name FROM role")
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Lỗi get_role: {e}")

    def get_role_name(self, role_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT role_name FROM role WHERE role_id = %s", (role_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return ""
        except Error as e:
            print(f"Lỗi get_role_name: '{e}'")

    def get_staff_names(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM staff")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except Error as e:
            print(f"Lỗi: '{e}'")
            return []
