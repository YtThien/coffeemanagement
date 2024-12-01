from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QHBoxLayout
from models.cart_model import CartModel

class InvoiceDialog(QDialog):
    def __init__(self, customer, staff_name, cart_model):
        super().__init__()
        self.customer = customer
        self.staff_name = staff_name
        self.cart_model = cart_model

        self.setWindowTitle("Hóa Đơn")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout(self)

        self.customer_label = QLabel(f"Thông tin khách hàng: {self.customer.name}, SĐT: {self.customer.phone}")
        self.staff_label = QLabel(f"Nhân viên tạo hóa đơn: {self.staff_name}")
        self.layout.addWidget(self.customer_label)
        self.layout.addWidget(self.staff_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        items = self.cart_model.get_items()
        if items:
            for item in items:
                item_widget = QWidget()
                item_layout = QHBoxLayout(item_widget)
                item_name_label = QLabel(f"{item['name']} - {item['price']}đ x {item['quantity']} = {item['total_price']}đ")
                item_layout.addWidget(item_name_label)
                item_widget.setLayout(item_layout)
                self.scroll_layout.addWidget(item_widget)

            total_amount = self.cart_model.calculate_total_amount()
            self.total_label = QLabel(f"Tổng tiền: {total_amount}đ")
            self.layout.addWidget(self.total_label)
        else:
            self.total_label = QLabel("Không có sản phẩm trong hóa đơn.")
            self.layout.addWidget(self.total_label)

        self.setLayout(self.layout)
