from PyQt6.QtWidgets import QMainWindow, QTableWidget, QPushButton, QLineEdit, QMessageBox, QTableWidgetItem, \
    QVBoxLayout, QWidget, QComboBox, QDoubleSpinBox, QDialog, QLabel, QDialogButtonBox, QApplication
from controllers.staff_controller import StaffController
from PyQt6 import QtCore, QtGui, QtWidgets


class StaffDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Staff")

        self.layout = QVBoxLayout(self)

        self.nameLabel = QLabel("Nhân Viên:", self)
        self.nameInput = QLineEdit(self)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.nameInput)

        self.phoneLabel = QLabel("Số Điện Thoại:", self)
        self.phoneInput = QLineEdit(self)
        self.layout.addWidget(self.phoneLabel)
        self.layout.addWidget(self.phoneInput)

        self.emailLabel = QLabel("Email:", self)
        self.emailInput = QLineEdit(self)
        self.layout.addWidget(self.emailLabel)
        self.layout.addWidget(self.emailInput)

        self.positionLabel = QLabel("Chức Vụ:", self)
        self.positionInput = QLineEdit(self)
        self.layout.addWidget(self.positionLabel)
        self.layout.addWidget(self.positionInput)

        self.userLabel = QLabel("UserName:", self)
        self.userInput = QLineEdit(self)
        self.layout.addWidget(self.userLabel)
        self.layout.addWidget(self.userInput)

        self.passLabel = QLabel("Password:", self)
        self.passInput = QLineEdit(self)
        self.layout.addWidget(self.passLabel)
        self.layout.addWidget(self.passInput)


        self.roleLabel = QLabel("Role", self)
        self.roleInput = QComboBox(self)
        self.layout.addWidget(self.roleLabel)
        self.layout.addWidget(self.roleInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        self.layout.addWidget(self.buttons)

        self.controller = StaffController()
        self.load_role()

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def load_role(self):
        roles = self.controller.get_role()
        for role in roles:
            self.roleInput.addItem(role[1], role[0])


    def getInputs(self):
        name = self.nameInput.text()
        phone = self.phoneInput.text()
        email = self.emailInput.text()
        position = self.positionInput.text()
        username = self.userInput.text()
        password = self.passInput.text()
        id_role = self.roleInput.currentData()
        return name,phone,email,position,username,password, id_role



class StaffView(QMainWindow):

    def __init__(self):
        super(StaffView,self).__init__()
        self.initUI()
        self.controller = StaffController()
        self.load_data()

    def initUI(self):
        self.setObjectName("MainWindow")
        self.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.tableView = QtWidgets.QTableWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(50, 50, 700, 400))
        self.tableView.setObjectName("tableView")
        self.tableView.setColumnCount(8)
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
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(7, item)

        self.btn_add = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add.setGeometry(QtCore.QRect(50, 470, 100, 30))
        self.btn_add.setObjectName("btn_add")
        self.btn_add.clicked.connect(self.add_staff)

        self.btn_edit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_edit.setGeometry(QtCore.QRect(160, 470, 100, 30))
        self.btn_edit.setObjectName("btn_edit")
        self.btn_edit.clicked.connect(self.update_staff)

        self.btn_delete = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete.setGeometry(QtCore.QRect(270, 470, 100, 30))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.clicked.connect(self.delete_staff)

        self.setCentralWidget(self.centralwidget)

        # self.controller = StaffController()
        # self.load_data()

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Staff Manager"))
        item = self.tableView.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableView.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Nhân Viên"))
        item = self.tableView.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Số Điện Thoại"))
        item = self.tableView.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Email"))
        item = self.tableView.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Chức vụ"))
        item = self.tableView.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "UserName"))
        item = self.tableView.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Password"))
        item = self.tableView.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Role"))
        self.btn_add.setText(_translate("MainWindow", "Thêm"))
        self.btn_edit.setText(_translate("MainWindow", "Sửa"))
        self.btn_delete.setText(_translate("MainWindow", "Xóa"))

    def load_data(self):
        staffs = self.controller.get_staff()
        self.tableView.setRowCount(len(staffs))
        self.tableView.setColumnCount(8)
        self.tableView.setHorizontalHeaderLabels(['ID', 'Nhân Viên', 'Số Điện Thoại', 'Email', 'Chức Vụ','UserName','Password','Role'])

        for row, staff in enumerate(staffs):
            self.tableView.setItem(row, 0, QTableWidgetItem(str(staff.id)))
            self.tableView.setItem(row, 1, QTableWidgetItem(staff.name_staff))
            self.tableView.setItem(row, 2, QTableWidgetItem(staff.phone))
            self.tableView.setItem(row, 3, QTableWidgetItem(staff.email))
            self.tableView.setItem(row, 4, QTableWidgetItem(staff.position))
            self.tableView.setItem(row, 5, QTableWidgetItem(staff.username))
            self.tableView.setItem(row, 6, QTableWidgetItem(staff.password))
            role_name = self.controller.get_role_name(staff.id_role)
            self.tableView.setItem(row, 7,QTableWidgetItem(role_name))
        self.tableView.resizeColumnsToContents()

    def add_staff(self):
        dialog = StaffDialog(self)
        if dialog.exec():
            name_staff,phone,email,position,username,password,id_role = dialog.getInputs()
            if name_staff:
                self.controller.create_staff(name_staff,phone,email,position,username,password,id_role)
                QMessageBox.information(self, "Thông báo", "Đã thêm thành công nhân viên")
                self.load_data()  # Reload dữ liệu sau khi thêm mới
            else:
                QMessageBox.warning(self, "Lỗi Nhập", "Tên và mô tả không được để trống")

    def update_staff(self):
        selected = self.tableView.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi Chọn", "Vui lòng chọn một Nhân viên để cập nhật")
            return

        id = self.tableView.item(selected,0).text()
        current_name = self.tableView.item(selected,1).text()
        current_phone = self.tableView.item(selected,2).text()
        current_email = self.tableView.item(selected, 3).text()
        current_position = self.tableView.item(selected,4).text()
        current_user = self.tableView.item(selected, 5).text()
        current_pass = self.tableView.item(selected, 6).text()
        current_role = self.tableView.item(selected, 7).text()

        dialog = StaffDialog(self)
        dialog.nameInput.setText(current_name)
        dialog.phoneInput.setText(current_phone)
        dialog.emailInput.setText(current_email)
        dialog.positionInput.setText(current_position)
        dialog.userInput.setText(current_user)
        dialog.passInput.setText(current_pass)


        index = dialog.roleInput.findText(current_role)
        if index != -1:
            dialog.roleInput.setCurrentIndex(index)

        if dialog.exec():
            name_staff,phone,email,position,username,password,id_role = dialog.getInputs()
            if name_staff and phone and username:
                self.controller.update_staff(id,name_staff,phone,email,position,username,password,id_role)
                QMessageBox.information(self,"Thông báo","Đã sửa thành công Nhân viên")
                self.load_data()
            else:
                QMessageBox.warning(self,"Lỗi Nhập","Không được để trống")

    def delete_staff(self):
        selected = self.tableView.currentRow()

        if selected == -1:
            QMessageBox.warning(self, "Lỗi Chọn", "Vui lòng chọn một danh mục để xóa")
            return
        reply = QMessageBox.question(self, "Remove Item", "Do you want to Remove Item ?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            id = self.tableView.item(selected, 0).text()

        self.controller.delete_staff(id)
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
#     window = StaffView()
#     window.initUI()
#     window.show()
#     sys.exit(app.exec())