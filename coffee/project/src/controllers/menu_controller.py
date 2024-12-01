from PyQt6.QtCore import QObject, pyqtSignal
from MySQLdb import Error
from models.menu_model import Menu
from database import create_connection

class MenuController(QObject):
    menu_updated = pyqtSignal()  # Tín hiệu phát ra khi menu được cập nhật

    def __init__(self):
        super().__init__()
        self.conn = create_connection()
        self.conn.autocommit(False)

    def create_menu(self, id_category, name_menu, price, description):
        try:
            cursor = self.conn.cursor()
            sql = '''INSERT INTO menu(id_category, name_menu, price, description)
                     VALUES (%s, %s, %s, %s)'''
            cursor.execute(sql, (id_category, name_menu, price, description))
            self.conn.commit()
            self.menu_updated.emit()  # Phát tín hiệu khi menu được cập nhật
            return cursor.lastrowid
        except Error as e:
            self.conn.rollback()  # Hoàn tác thay đổi nếu có lỗi
            print(f"Lỗi: '{e}'")

    def get_menu(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM menu")
            rows = cursor.fetchall()
            return [Menu(*row) for row in rows]
        except Error as e:
            print(f"Lỗi: '{e}'")

    def get_menu_category(self, id_category):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM menu WHERE id_category = %s", (id_category,))
            rows = cursor.fetchall()
            return [Menu(*row) for row in rows]
        except Error as e:
            print(f"Lỗi: '{e}'")

    def update_menu(self, id, id_category, name_menu, price, description):
        try:
            cursor = self.conn.cursor()
            sql = '''UPDATE menu SET id_category = %s, name_menu = %s, price = %s, description = %s
                     WHERE id = %s'''
            cursor.execute(sql, (id_category, name_menu, price, description, id))
            self.conn.commit()
            self.menu_updated.emit()  # Phát tín hiệu khi menu được cập nhật
        except Error as e:
            self.conn.rollback()  # Hoàn tác thay đổi nếu có lỗi
            print(f"Lỗi: '{e}'")

    def delete_menu(self, id):
        try:
            cursor = self.conn.cursor()
            sql = 'DELETE FROM menu WHERE id = %s'
            cursor.execute(sql, (id,))
            self.conn.commit()
            self.menu_updated.emit()  # Phát tín hiệu khi menu được cập nhật
        except Error as e:
            self.conn.rollback()  # Hoàn tác thay đổi nếu có lỗi
            print(f"Lỗi: '{e}'")

    def get_categories(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name_category FROM category")
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Lỗi: {e}")

    def get_category_name(self, id_category):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name_category FROM category WHERE id = %s", (id_category,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return ""
        except Error as e:
            print(f"Lỗi: '{e}'")
