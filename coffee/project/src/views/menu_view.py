from PyQt6.QtWidgets import QMainWindow, QTableWidget, QPushButton, QLineEdit, QMessageBox, QTableWidgetItem, \
    QVBoxLayout, QWidget, QComboBox, QDoubleSpinBox, QDialog, QLabel, QDialogButtonBox, QApplication
from controllers.menu_controller import MenuController
from PyQt6 import QtCore, QtGui, QtWidgets

class MenuDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Menu")

        self.layout = QVBoxLayout(self)

        self.cateLabel = QLabel("Danh Mục", self)
        self.cateInput = QComboBox(self)
        self.layout.addWidget(self.cateLabel)
        self.layout.addWidget(self.cateInput)

        self.nameLabel = QLabel("Tên Món:", self)
        self.nameInput = QLineEdit(self)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.nameInput)

        self.priceLabel = QLabel("Giá Tiền:", self)
        self.priceInput = QDoubleSpinBox(self)
        self.priceInput.setDecimals(2)
        self.priceInput.setMaximum(999999999.99)
        self.layout.addWidget(self.priceLabel)
        self.layout.addWidget(self.priceInput)

        self.descriptionLabel = QLabel("Mô tả:", self)
        self.descriptionInput = QLineEdit(self)
        self.layout.addWidget(self.descriptionLabel)
        self.layout.addWidget(self.descriptionInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        self.layout.addWidget(self.buttons)

        self.controller = MenuController()
        self.load_categories()

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def load_categories(self):
        categories = self.controller.get_categories()
        for category in categories:
            self.cateInput.addItem(category[1], category[0])

    def getInputs(self):
        category_id = self.cateInput.currentData()
        name = self.nameInput.text()
        price = self.priceInput.value()
        description = self.descriptionInput.text()
        return category_id, name, price, description


class MenuView(QMainWindow):
    def __init__(self):
        super(MenuView,self).__init__()
        self.initUI()
        self.controller = MenuController()
        self.load_data()

    def initUI(self):
        self.setObjectName("MainWindow")
        self.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.tableView = QtWidgets.QTableWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(50, 50, 600, 400))
        self.tableView.setObjectName("tableView")
        self.tableView.setColumnCount(5)
        self.tableView.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(4, item)

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

        # self.controller = MenuController()
        # self.load_data()

        self.retranslateUi()

        self.btn_add.clicked.connect(self.add_menu)
        self.btn_edit.clicked.connect(self.update_menu)
        self.btn_delete.clicked.connect(self.delete_menu)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Menu Manager"))
        item = self.tableView.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableView.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Danh Mục"))
        item = self.tableView.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Tên Món"))
        item = self.tableView.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Giá"))
        item = self.tableView.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Mô tả"))
        self.btn_add.setText(_translate("MainWindow", "Thêm"))
        self.btn_edit.setText(_translate("MainWindow", "Sửa"))
        self.btn_delete.setText(_translate("MainWindow", "Xóa"))

    def load_data(self):
        menus = self.controller.get_menu()
        self.tableView.setRowCount(len(menus))
        self.tableView.setColumnCount(5)
        self.tableView.setHorizontalHeaderLabels(['ID', 'Danh Mục', 'Tên Món', 'Giá', 'Mô tả'])

        for row, menu in enumerate(menus):
            self.tableView.setItem(row, 0, QTableWidgetItem(str(menu.id)))
            category_name = self.controller.get_category_name(menu.id_category)
            self.tableView.setItem(row, 1, QTableWidgetItem(category_name))  # Hiển thị category_name thay vì id_category
            self.tableView.setItem(row, 2, QTableWidgetItem(menu.name_menu))
            self.tableView.setItem(row, 3, QTableWidgetItem(str(menu.price)))
            self.tableView.setItem(row, 4, QTableWidgetItem(menu.description))
        self.tableView.resizeColumnsToContents()


    def add_menu(self):
        dialog = MenuDialog(self)
        if dialog.exec():
            category_id, name, price, description = dialog.getInputs()
            if name:
                self.controller.create_menu(category_id, name, price, description)
                QMessageBox.information(self, "Thông báo", "Đã thêm thành công món ăn")
                self.load_data()  # Reload dữ liệu sau khi thêm mới
            else:
                QMessageBox.warning(self, "Lỗi Nhập", "Tên và mô tả không được để trống")

    def update_menu(self):
        selected = self.tableView.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi Chọn", "Vui lòng chọn một Món ăn để cập nhật")
            return

        id = self.tableView.item(selected,0).text()
        current_category = self.tableView.item(selected,1).text()
        current_name = self.tableView.item(selected,2).text()
        current_price = float(self.tableView.item(selected,3).text())
        current_description = self.tableView.item(selected,4).text()

        dialog = MenuDialog(self)
        dialog.nameInput.setText(current_name)
        dialog.priceInput.setValue(current_price)
        dialog.descriptionInput.setText(current_description)

        index = dialog.cateInput.findText(current_category)
        if index != -1:
            dialog.cateInput.setCurrentIndex(index)

        if dialog.exec():
            category_id, name, price, description = dialog.getInputs()
            if category_id and name and price:
                self.controller.update_menu(id,category_id,name,price,description)
                QMessageBox.information(self,"Thông báo","Đã sửa thành công Món ăn")
                self.load_data()
            else:
                QMessageBox.warning(self,"Lỗi Nhập","Không được để trống")


    def delete_menu(self):
        selected = self.tableView.currentRow()

        if selected == -1:
            QMessageBox.warning(self, "Lỗi Chọn", "Vui lòng chọn một danh mục để xóa")
            return
        reply = QMessageBox.question(self, "Remove Item", "Do you want to Remove Item ?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            id = self.tableView.item(selected, 0).text()

        self.controller.delete_menu(id)
        # self.tableView.removeRow(selected)
        QMessageBox.information(self, "Thông báo", "Đã xóa thành công danh mục")

        self.load_data()  # Reload dữ liệu sau khi xóa

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Thông báo',
                                     "Bạn có chắc muốn thoát?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     window = MenuView()
#     window.initUI()
#     window.show()
#     sys.exit(app.exec())
