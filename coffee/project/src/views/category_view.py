from PyQt6.QtWidgets import QMainWindow, QTableWidget, QPushButton, QLineEdit, QMessageBox, QTableWidgetItem, \
    QVBoxLayout, QWidget, QInputDialog, QDialog, QLabel, QDialogButtonBox
from controllers.category_controller import CategoryController
from PyQt6 import QtCore, QtGui, QtWidgets


class CategoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Danh Mục")

        self.layout = QVBoxLayout(self)

        self.nameLabel = QLabel("Tên Danh Mục:", self)
        self.nameInput = QLineEdit(self)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.nameInput)

        self.descriptionLabel = QLabel("Mô Tả Danh Mục:", self)
        self.descriptionInput = QLineEdit(self)
        self.layout.addWidget(self.descriptionLabel)
        self.layout.addWidget(self.descriptionInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                        self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def getInputs(self):
        return self.nameInput.text(), self.descriptionInput.text()


class CategoryView(QMainWindow):
    def __init__(self):
        super(CategoryView, self).__init__()
        self.controller = CategoryController()  # Khởi tạo controller
        self.controller.category_updated.connect(self.load_data)  # Kết nối tín hiệu
        self.initUI()
        self.load_data()  # Load dữ liệu ban đầu

    def initUI(self):
        self.setObjectName("MainWindow")
        self.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.tableView = QtWidgets.QTableWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(50, 50, 600, 400))
        self.tableView.setObjectName("tableView")
        self.tableView.setColumnCount(3)
        self.tableView.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(2, item)

        self.btn_add = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add.setGeometry(QtCore.QRect(50, 470, 100, 30))
        self.btn_add.setObjectName("btn_add")

        self.btn_edit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_edit.setGeometry(QtCore.QRect(160, 470, 100, 30))
        self.btn_edit.setObjectName("btn_edit")

        self.btn_delete = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete.setGeometry(QtCore.QRect(270, 470, 100, 30))
        self.btn_delete.setObjectName("btn_delete")

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()

        self.btn_add.clicked.connect(self.add_category)
        self.btn_edit.clicked.connect(self.update_category)
        self.btn_delete.clicked.connect(self.delete_category)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableView.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableView.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Danh Mục"))
        item = self.tableView.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Mô tả"))
        self.btn_add.setText(_translate("MainWindow", "Thêm"))
        self.btn_edit.setText(_translate("MainWindow", "Sửa"))
        self.btn_delete.setText(_translate("MainWindow", "Xóa"))

    def load_data(self):
        categories = self.controller.get_all_categories()
        self.tableView.setRowCount(len(categories))
        self.tableView.setColumnCount(3)
        self.tableView.setHorizontalHeaderLabels(['ID', 'Tên', 'Mô tả'])

        for row, category in enumerate(categories):
            self.tableView.setItem(row, 0, QTableWidgetItem(str(category.id)))
            self.tableView.setItem(row, 1, QTableWidgetItem(category.name_category))
            self.tableView.setItem(row, 2, QTableWidgetItem(category.description))
        self.tableView.resizeColumnsToContents()

    def add_category(self):
        dialog = CategoryDialog(self)
        if dialog.exec():
            name, description = dialog.getInputs()
            if name:
                self.controller.create_category(name, description)
                QMessageBox.information(self, "Thông báo", "Đã thêm thành công danh mục")
                # Không cần gọi self.load_data() vì tín hiệu sẽ tự động gọi
            else:
                QMessageBox.warning(self, "Lỗi Nhập", "Tên và mô tả không được để trống")

    def update_category(self):
        selected = self.tableView.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi Chọn", "Vui lòng chọn một danh mục để cập nhật")
            return

        id = self.tableView.item(selected, 0).text()
        current_name = self.tableView.item(selected, 1).text()
        current_description = self.tableView.item(selected, 2).text()

        dialog = CategoryDialog(self)
        dialog.nameInput.setText(current_name)
        dialog.descriptionInput.setText(current_description)

        if dialog.exec():
            name, description = dialog.getInputs()
            if name:
                self.controller.update_category(id, name, description)
                QMessageBox.information(self, "Thông báo", "Đã sửa thành công danh mục")

                # Không cần gọi self.load_data() vì tín hiệu sẽ tự động gọi
            else:
                QMessageBox.warning(self, "Lỗi Nhập", "Tên và mô tả không được để trống")

    def delete_category(self):
        selected = self.tableView.currentRow()

        if selected == -1:
            QMessageBox.warning(self, "Lỗi Chọn", "Vui lòng chọn một danh mục để xóa")
            return
        reply = QMessageBox.question(self, "Remove Item", "Do you want to Remove Item ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            id = self.tableView.item(selected, 0).text()

            self.controller.delete_category(id)
            self.tableView.removeRow(selected)
            QMessageBox.information(self, "Thông báo", "Đã xóa thành công danh mục")
            # Không cần gọi self.load_data() vì tín hiệu sẽ tự động gọi

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Thông báo',
                                     "Bạn có chắc muốn thoát?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
