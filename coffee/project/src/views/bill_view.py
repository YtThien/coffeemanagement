from PyQt6.QtWidgets import QMainWindow, QTableWidget, QPushButton, QMessageBox, QTableWidgetItem, \
    QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QLabel, QHeaderView
from controllers.bill_controller import BillController

class BillView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.controller = BillController()
        self.load_data()

    def initUI(self):
        self.setWindowTitle("Quản lý Hóa đơn")
        self.resize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Tìm kiếm theo số điện thoại
        search_layout = QHBoxLayout()
        search_label = QLabel("Số điện thoại:")
        self.search_input = QLineEdit()
        search_button = QPushButton("Tìm kiếm")
        search_button.clicked.connect(self.search_bills)
        reset_button = QPushButton("Hiển thị tất cả")
        reset_button.clicked.connect(self.load_data)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(reset_button)

        layout.addLayout(search_layout)

        # Bảng hiển thị hóa đơn
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Khách hàng", "Số điện thoại", "Nhân viên", "Ngày tạo", "Tổng tiền"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)

        # Bảng hiển thị chi tiết hóa đơn
        self.detail_table = QTableWidget()
        self.detail_table.setColumnCount(3)
        self.detail_table.setHorizontalHeaderLabels(["Món", "Số lượng", "Giá"])
        self.detail_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.detail_table)

        # Bắt sự kiện khi nhấn vào hóa đơn trong bảng
        self.table.cellClicked.connect(self.show_bill_detail)

    def load_data(self):
        bills = self.controller.get_bills()
        self.table.setRowCount(len(bills))

        for row, bill in enumerate(bills):
            self.table.setItem(row, 0, QTableWidgetItem(str(bill.id)))
            self.table.setItem(row, 1, QTableWidgetItem(self.controller.get_customer_name(bill.id_customer) or "-"))
            self.table.setItem(row, 2, QTableWidgetItem(self.controller.get_customer_phone(bill.id_customer) or "-"))
            self.table.setItem(row, 3, QTableWidgetItem(self.controller.get_staff_name(bill.id_staff) or "-"))
            self.table.setItem(row, 4, QTableWidgetItem(str(bill.date)))
            self.table.setItem(row, 5, QTableWidgetItem(str(bill.total)))

    def search_bills(self):
        phone_number = self.search_input.text()
        if phone_number:
            bills = self.controller.search_bills_by_phone(phone_number)
            self.table.setRowCount(len(bills))

            for row, bill in enumerate(bills):
                self.table.setItem(row, 0, QTableWidgetItem(str(bill.id)))
                self.table.setItem(row, 1, QTableWidgetItem(self.controller.get_customer_name(bill.id_customer) or "-"))
                self.table.setItem(row, 2, QTableWidgetItem(self.controller.get_customer_phone(bill.id_customer) or "-"))
                self.table.setItem(row, 3, QTableWidgetItem(self.controller.get_staff_name(bill.id_staff) or "-"))
                self.table.setItem(row, 4, QTableWidgetItem(str(bill.date)))
                self.table.setItem(row, 5, QTableWidgetItem(str(bill.total)))
            self.search_input.clear()  # Xóa nội dung của ô tìm kiếm sau khi tìm kiếm thành công
    def show_bill_detail(self, row, column):
        bill_id = int(self.table.item(row, 0).text())
        bill_details = self.controller.get_bill_details(bill_id)
        self.detail_table.setRowCount(len(bill_details))

        for row, item in enumerate(bill_details):
            self.detail_table.setItem(row, 0, QTableWidgetItem(item.menu_name))
            self.detail_table.setItem(row, 1, QTableWidgetItem(str(item.quantity)))
            self.detail_table.setItem(row, 2, QTableWidgetItem(str(item.price)))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Thông báo',
                                     "Bạn có chắc muốn thoát?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

# Chạy ứng dụng
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = BillView()
    window.show()
    sys.exit(app.exec())
