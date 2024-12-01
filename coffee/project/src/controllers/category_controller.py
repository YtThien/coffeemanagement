from PyQt6.QtCore import QObject, pyqtSignal
from MySQLdb import Error
from models.category_model import Category
from database import create_connection

class CategoryController(QObject):  # Kế thừa từ QObject
    category_updated = pyqtSignal()

    def __init__(self, parent=None):  # Thêm parent=None để tương thích với QObject
        super().__init__(parent)
        self.conn = create_connection()

    def create_category(self, name_category, description):
        try:
            cursor = self.conn.cursor()
            sql = '''INSERT INTO category(name_category, description)
                     VALUES(%s, %s)'''
            cursor.execute(sql, (name_category, description))
            self.conn.commit()
            self.category_updated.emit()  # Sử dụng tín hiệu emit
            return cursor.lastrowid
        except Error as e:
            print(f"Lỗi: '{e}'")

    def get_all_categories(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM category")
            rows = cursor.fetchall()
            return [Category(*row) for row in rows]
        except Error as e:
            print(f"Lỗi: '{e}'")

    def update_category(self, id, name_category, description):
        try:
            cursor = self.conn.cursor()
            sql = '''UPDATE category SET name_category = %s, description = %s WHERE id = %s'''
            cursor.execute(sql, (name_category, description, id))
            self.conn.commit()
            self.category_updated.emit()  # Sử dụng tín hiệu emit
        except Error as e:
            print(f"Lỗi: '{e}'")

    def delete_category(self, id):
        try:
            cursor = self.conn.cursor()
            sql = 'DELETE FROM category WHERE id = %s'
            cursor.execute(sql, (id,))
            self.conn.commit()
            self.category_updated.emit()  # Sử dụng tín hiệu emit
        except Error as e:
            print(f"Lỗi: '{e}'")
