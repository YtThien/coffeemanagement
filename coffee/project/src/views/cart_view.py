from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QSpinBox, QHeaderView, QLabel
from PyQt6.QtCore import Qt

class CartView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Giỏ hàng
        self.cart_layout = QVBoxLayout()
        self.setLayout(self.cart_layout)

        self.cart = QTableWidget()
        self.cart.setColumnCount(5)  # Thêm cột cho nút Xóa
        self.cart.setHorizontalHeaderLabels(['Tên sản phẩm', 'Giá', 'Số lượng', 'Tổng giá', 'Xóa'])
        self.cart.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Co giãn cột
        self.cart.horizontalHeader().setStretchLastSection(True)  # Cột cuối cùng co giãn
        self.cart_layout.addWidget(self.cart)

        self.update_cart_view([])  # Khởi tạo giỏ hàng rỗng

    def add_to_cart(self, name, price):
        self.controller.add_to_cart(name, price)
        self.update_cart_view(self.controller.get_cart_items())

    def update_quantity(self, quantity, row):
        self.controller.update_total_price(row, quantity)
        self.update_cart_view(self.controller.get_cart_items())

    def remove_from_cart(self, row):
        self.controller.remove_from_cart(row)
        self.update_cart_view(self.controller.get_cart_items())

    def update_cart_view(self, cart_items):
        self.cart.setRowCount(len(cart_items))

        for row, item in enumerate(cart_items):
            name = item['name']
            price = item['price']
            quantity = item['quantity']
            total_price = item['total_price']

            name_item = QTableWidgetItem(name)
            price_item = QTableWidgetItem(str(price))
            quantity_item = QSpinBox()  # Đổi lại thành QSpinBox
            quantity_item.setValue(quantity)
            quantity_item.setMinimum(1)  # Đặt số lượng tối thiểu là 1
            quantity_item.valueChanged.connect(lambda value, r=row: self.update_quantity(value, r))
            total_price_item = QTableWidgetItem(str(total_price))
            remove_button = QPushButton("Xóa")
            remove_button.clicked.connect(lambda _, r=row: self.remove_from_cart(r))

            self.cart.setItem(row, 0, name_item)
            self.cart.setItem(row, 1, price_item)
            self.cart.setCellWidget(row, 2, quantity_item)  # Sử dụng setCellWidget để đặt QSpinBox
            self.cart.setItem(row, 3, total_price_item)
            self.cart.setCellWidget(row, 4, remove_button)

    def load_cart_items(self):
        self.update_cart_view(self.controller.get_cart_items())

    def update_view(self):
        self.load_cart_items()  # Gọi lại phương thức tải các sản phẩm trong giỏ hàng
