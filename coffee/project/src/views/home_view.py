from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QMessageBox, QLabel, QLineEdit, QScrollArea, QSizePolicy, QDialog
from cart_view import CartView
from controllers.cart_controller import CartController
from models.cart_model import CartModel
from controllers.staff_controller import StaffController
from controllers.customer_controller import CustomerController
from views.bill_cus import InvoiceDialog

class HomeView(QWidget):
    def __init__(self, controller, conn):
        super().__init__()
        self.controller = controller
        self.conn = conn
        self.staff_controller = StaffController(self.conn)
        self.customer_controller = CustomerController(self.conn)
        self.invoice_dialog = None

        self.home_layout = QVBoxLayout()
        self.setLayout(self.home_layout)

        self.customer_layout = QHBoxLayout()
        self.customer_name_label = QLabel("Tên khách hàng:")
        self.customer_name_input = QLineEdit()
        self.customer_layout.addWidget(self.customer_name_label)
        self.customer_layout.addWidget(self.customer_name_input)

        self.customer_phone_label = QLabel("Số điện thoại:")
        self.customer_phone_input = QLineEdit()
        self.customer_layout.addWidget(self.customer_phone_label)
        self.customer_layout.addWidget(self.customer_phone_input)

        self.home_layout.addLayout(self.customer_layout)

        self.staff_layout = QHBoxLayout()
        self.staff_name_label = QLabel("Tên nhân viên tạo hóa đơn:")
        self.staff_name_input = QLineEdit()
        self.staff_layout.addWidget(self.staff_name_label)
        self.staff_layout.addWidget(self.staff_name_input)

        self.home_layout.addLayout(self.staff_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.home_layout.addWidget(self.scroll_area)

        self.menu_tabs = QTabWidget()
        self.menu_tabs.currentChanged.connect(self.load_menu_items)
        self.scroll_area.setWidget(self.menu_tabs)

        self.cart_model = CartModel()
        self.cart_controller = CartController(self.cart_model, self.conn)

        self.cart_view = CartView(self.cart_controller)
        self.home_layout.addWidget(self.cart_view)

        self.create_bill_button = QPushButton("Tạo Hóa Đơn")
        self.create_bill_button.clicked.connect(self.create_bill_dialog)
        self.home_layout.addWidget(self.create_bill_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_menu)
        self.home_layout.addWidget(self.refresh_button)

        self.message_label = QLabel("")
        self.home_layout.addWidget(self.message_label)

        self.reload_menu_tabs()

    def load_data(self):
        try:
            categories = self.controller.get_categories()
            for category in categories:
                category_id, category_name = category
                tab = QWidget()
                tab.setObjectName(str(category_id))
                self.menu_tabs.addTab(tab, category_name)
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu danh mục: {e}")

    def refresh_menu(self):
        try:
            self.menu_tabs.clear()
            self.load_data()
        except Exception as e:
            print(f"Lỗi khi refresh menu: {e}")

    def reload_menu_tabs(self):
        try:
            self.menu_tabs.clear()
            categories = self.controller.get_categories()
            for category in categories:
                category_id, category_name = category
                tab = QWidget()
                tab.setObjectName(str(category_id))
                self.menu_tabs.addTab(tab, category_name)

        except Exception as e:
            print(f"Lỗi khi tải dữ liệu danh mục: {e}")

    def load_menu_items(self, index):
        try:
            if index < 0 or index >= self.menu_tabs.count():
                print(f"Invalid tab index: {index}")
                return

            tab = self.menu_tabs.widget(index)

            if tab is None:
                print(f"Tab at index {index} is None.")
                return

            category_id = int(tab.objectName())
            menu_items = self.controller.get_menu_category(category_id)

            tab_layout = QVBoxLayout(tab)
            tab.setLayout(tab_layout)

            for item in menu_items:
                name = item.name_menu
                price = item.price
                button = QPushButton(f"{name} - {price}")
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                button.clicked.connect(lambda _, n=name, p=price: self.cart_view.add_to_cart(n, p))
                tab_layout.addWidget(button)

        except Exception as e:
            print(f"Lỗi khi tải các món trong danh mục: {e}")

    def create_bill_dialog(self):
        customer_name = self.customer_name_input.text().strip()
        customer_phone = self.customer_phone_input.text().strip()

        if customer_name and customer_phone:
            existing_customer = self.customer_controller.get_customer_by_name_phone(customer_name, customer_phone)
            if existing_customer:
                selected_customer = existing_customer
            else:
                selected_customer = self.customer_controller.create_customer(customer_name, customer_phone)
        else:
            selected_customer = self.customer_controller.get_customer_by_id(1)

        staff_name = self.staff_name_input.text().strip()

        if not staff_name:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tên nhân viên tạo hóa đơn.")
            return

        success = self.cart_controller.create_bill(selected_customer.id, staff_name)

        if success:
            # Hóa đơn đã được tạo thành công, hiển thị hộp thoại hóa đơn
            self.show_invoice(selected_customer, staff_name)

            self.clear_inputs()
            self.cart_model.clear_cart()
            self.cart_view.update_view()
        else:
            self.message_label.setText("Có lỗi xảy ra trong quá trình tạo hóa đơn.")

    def show_invoice(self, customer, staff_name):
        # Tạo hộp thoại hóa đơn
        invoice_dialog = InvoiceDialog(customer, staff_name, self.cart_model)
        invoice_dialog.exec()

    def clear_inputs(self):
        self.customer_name_input.clear()
        self.customer_phone_input.clear()
        self.staff_name_input.clear()
