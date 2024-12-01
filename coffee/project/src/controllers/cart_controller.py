from PyQt6.QtWidgets import QMessageBox
from models.cart_model import CartModel
from database import create_connection

class CartController:
    def __init__(self, cart_model, conn):
        self.cart_model = cart_model
        self.conn = conn

    def add_to_cart(self, name, price):
        self.cart_model.add_item(name, price)

    def update_total_price(self, index, quantity):
        self.cart_model.update_item_quantity(index, quantity)

    def remove_from_cart(self, index):
        self.cart_model.remove_item(index)

    def get_cart_items(self):
        return self.cart_model.get_items()

    def create_bill(self, customer_id, staff_name):
        items = self.cart_model.get_items()
        if not items:
            QMessageBox.warning(None, "Thông báo", "Giỏ hàng trống!")
            return False

        try:
            cursor = self.conn.cursor()

            # Lấy id_staff từ tên nhân viên
            staff_id = self.get_staff_id_by_name(staff_name)

            # Tạo hóa đơn trong bảng `bill`
            sql_bill = '''INSERT INTO bill (id_customer, id_staff, total, date)
                          VALUES (%s, %s, %s, current_timestamp())'''
            total_amount = sum(item['total_price'] for item in items)

            cursor.execute(sql_bill, (customer_id, staff_id, total_amount))
            bill_id = cursor.lastrowid

            # Lưu chi tiết hóa đơn trong bảng `bill_detail`
            sql_bill_detail = '''INSERT INTO bill_detail (id_bill, id_menu, quantity, price)
                                 VALUES (%s, %s, %s, %s)'''

            for item in items:
                id_menu = self.get_menu_id_by_name(item['name'])  # Lấy id_menu từ tên món ăn
                quantity = item['quantity']
                price = item['price']

                cursor.execute(sql_bill_detail, (bill_id, id_menu, quantity, price))

            # Lưu thay đổi vào cơ sở dữ liệu
            self.conn.commit()

            # Xóa giỏ hàng sau khi đã tạo hóa đơn thành công
            self.cart_model.clear_cart()

            return True

        except Exception as e:
            print(f"Lỗi khi tạo hóa đơn: {e}")
            QMessageBox.warning(None, "Thông báo", "Có lỗi xảy ra khi tạo hóa đơn!")
            return False

    def get_menu_id_by_name(self, menu_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM menu WHERE name_menu = %s", (menu_name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError(f"Không tìm thấy món ăn có tên '{menu_name}' trong cơ sở dữ liệu.")
        except Exception as e:
            print(f"Lỗi khi truy vấn menu từ tên: {e}")
            raise

    def get_staff_id_by_name(self, staff_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM staff WHERE name = %s", (staff_name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError(f"Không tìm thấy nhân viên có tên '{staff_name}' trong cơ sở dữ liệu.")
        except Exception as e:
            print(f"Lỗi khi truy vấn nhân viên từ tên: {e}")
            raise
