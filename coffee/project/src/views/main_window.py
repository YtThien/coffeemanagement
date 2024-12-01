import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, \
    QStackedWidget, QLabel, QLineEdit, QMessageBox, QDialog
from PyQt6.QtCore import Qt

from controllers.bill_controller import BillController
from controllers.menu_controller import MenuController
from database import create_connection
from views.bill_view import BillView
from views.category_view import CategoryView
from views.home_view import HomeView
from views.menu_view import MenuView
from views.report_view import ReportView
from views.staff_view import StaffView
from views.customer_view import CustomerView


# Import các class từ các module và package còn thiếu

# class LoginWindow(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Đăng nhập")
#         self.username_edit = QLineEdit(self)
#         self.password_edit = QLineEdit(self)
#         self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
#
#         layout = QVBoxLayout(self)
#         layout.addWidget(QLabel("Tên đăng nhập:"))
#         layout.addWidget(self.username_edit)
#         layout.addWidget(QLabel("Mật khẩu:"))
#         layout.addWidget(self.password_edit)
#
#         self.login_button = QPushButton("Đăng nhập", self)
#         self.login_button.clicked.connect(self.login)
#
#         layout.addWidget(self.login_button)
#         self.setLayout(layout)
#
#         # Biến để lưu trạng thái đăng nhập
#         self.login_successful = False
#
#     def login(self):
#         username = self.username_edit.text().strip()
#         password = self.password_edit.text().strip()
#
#         if username == "admin" and password == "adminpassword":
#             QMessageBox.information(self, "Đăng nhập thành công", "Đăng nhập thành công!")
#             self.login_successful = True
#             self.accept()  # Chấp nhận và đóng cửa sổ đăng nhập sau khi đăng nhập thành công
#         else:
#             QMessageBox.warning(self, "Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")
#
#             # Đặt lại trường nhập liệu để người dùng có thể thử lại
#             self.username_edit.clear()
#             self.password_edit.clear()
#             self.username_edit.setFocus()
#
#     def was_login_successful(self):
#         return self.login_successful

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.conn = create_connection()
        self.controller = MenuController()
        self.controller.menu_updated.connect(self.reload_menu_tabs)
        self.setWindowTitle('Hệ Thống Quản Lý Cafe')
        self.resize(1200, 800)

        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        buttons = ['Trang chủ', 'Kho', 'Quản Lý', 'Hóa đơn', 'Thống kê', 'Cài đặt']
        for button in buttons:
            btn = QPushButton(button)
            btn.clicked.connect(self.change_page)
            sidebar_layout.addWidget(btn)

        main_layout.addWidget(sidebar)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.home_view = HomeView(self.controller, self.conn)
        self.stacked_widget.addWidget(self.home_view)

        self.manager_tab_widget = QTabWidget()
        self.category_view = CategoryView()
        self.manager_tab_widget.addTab(self.category_view, "Category")
        self.menu_view = MenuView()
        self.manager_tab_widget.addTab(self.menu_view, "Menu")
        self.staff_view = StaffView()
        self.manager_tab_widget.addTab(self.staff_view, "Staff")
        self.customer_view = CustomerView()
        self.manager_tab_widget.addTab(self.customer_view, "Customer")

        self.stacked_widget.addWidget(self.manager_tab_widget)

        self.bill_controller = BillController()
        self.bill_view = BillView()
        self.stacked_widget.addWidget(self.bill_view)
        self.stacked_widget.setCurrentWidget(self.home_view)

        self.report_view = ReportView()
        self.stacked_widget.addWidget(self.report_view)
        self.stacked_widget.setCurrentWidget(self.home_view)

    # def reload_menu_tabs(self):
    #     current_index = self.home_view.menu_tabs.currentIndex()
    #     self.home_view.menu_tabs.clear()
    #     self.home_view.load_categories()
    #     self.home_view.menu_tabs.setCurrentIndex(current_index)

    def reload_menu_tabs(self):
        current_index = self.stacked_widget.currentIndex()

        if current_index == self.stacked_widget.indexOf(self.home_view):
            self.home_view.menu_tabs.clear()  # Xóa tất cả các tab hiện tại

            try:
                categories = self.controller.get_categories()
                for category_id, category_name in categories:
                    tab = QWidget()
                    tab.setObjectName(str(category_id))
                    self.home_view.menu_tabs.addTab(tab, category_name)
            except Exception as e:
                print(f"Lỗi khi tải dữ liệu danh mục: {e}")

            # Cập nhật lại danh sách món ăn cho tab hiện tại
            self.home_view.load_menu_items(self.home_view.menu_tabs.currentIndex())

    # def show_login_dialog(self):
    #     login_dialog = LoginWindow(self)
    #     login_dialog.exec()  # Hiển thị cửa sổ đăng nhập dưới dạng QDialog
    #
    #     # Kiểm tra xem đăng nhập thành công hay không
    #     if login_dialog.was_login_successful():
    #         return True
    #     else:
    #         return False

    def change_page(self):
        # if not self.show_login_dialog():
        #     return

        sender = self.sender()
        page_dict = {
            'Trang chủ': self.home_view,
            'Kho': self.home_view,
            'Quản Lý': self.manager_tab_widget,
            'Hóa đơn': self.bill_view,
            'Thống kê': self.report_view,
            'Cài đặt': self.home_view
        }
        widget = page_dict.get(sender.text())
        if widget is not None:
            self.stacked_widget.setCurrentWidget(widget)
        else:
            print("Không tìm thấy trang tương ứng.")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
