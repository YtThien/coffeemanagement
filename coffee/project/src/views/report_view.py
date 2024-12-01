from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget, QHeaderView
from controllers.bill_controller import BillController

class ReportView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = BillController()
        self.initUI()
        self.load_daily_revenue()
        self.load_weekly_revenue()
        self.load_monthly_revenue()

    def initUI(self):
        self.setWindowTitle("Báo cáo và Thống kê")
        self.resize(1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Tab Doanh thu hàng ngày
        self.daily_tab = QWidget()
        self.daily_layout = QVBoxLayout(self.daily_tab)
        self.daily_revenue_table = QTableWidget()
        self.daily_revenue_table.setColumnCount(2)
        self.daily_revenue_table.setHorizontalHeaderLabels(["Ngày", "Doanh thu"])
        self.daily_revenue_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.daily_layout.addWidget(self.daily_revenue_table)

        # Bảng xu hướng bán hàng hàng ngày
        self.daily_trend_table = QTableWidget()
        self.daily_trend_table.setColumnCount(3)
        self.daily_trend_table.setHorizontalHeaderLabels(["Món", "Số lượng", "Tổng tiền"])
        self.daily_trend_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.daily_layout.addWidget(self.daily_trend_table)

        self.tabs.addTab(self.daily_tab, "Doanh thu hàng ngày")

        # Tab Doanh thu hàng tuần
        self.weekly_tab = QWidget()
        self.weekly_layout = QVBoxLayout(self.weekly_tab)
        self.weekly_revenue_table = QTableWidget()
        self.weekly_revenue_table.setColumnCount(3)
        self.weekly_revenue_table.setHorizontalHeaderLabels(["Năm", "Tuần", "Doanh thu"])
        self.weekly_revenue_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.weekly_layout.addWidget(self.weekly_revenue_table)

        # Bảng xu hướng bán hàng hàng tuần
        self.weekly_trend_table = QTableWidget()
        self.weekly_trend_table.setColumnCount(3)
        self.weekly_trend_table.setHorizontalHeaderLabels(["Món", "Số lượng", "Tổng tiền"])
        self.weekly_trend_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.weekly_layout.addWidget(self.weekly_trend_table)

        self.tabs.addTab(self.weekly_tab, "Doanh thu hàng tuần")

        # Tab Doanh thu hàng tháng
        self.monthly_tab = QWidget()
        self.monthly_layout = QVBoxLayout(self.monthly_tab)
        self.monthly_revenue_table = QTableWidget()
        self.monthly_revenue_table.setColumnCount(3)
        self.monthly_revenue_table.setHorizontalHeaderLabels(["Năm", "Tháng", "Doanh thu"])
        self.monthly_revenue_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.monthly_layout.addWidget(self.monthly_revenue_table)

        # Bảng xu hướng bán hàng hàng tháng
        self.monthly_trend_table = QTableWidget()
        self.monthly_trend_table.setColumnCount(3)
        self.monthly_trend_table.setHorizontalHeaderLabels(["Món", "Số lượng", "Tổng tiền"])
        self.monthly_trend_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.monthly_layout.addWidget(self.monthly_trend_table)

        self.tabs.addTab(self.monthly_tab, "Doanh thu hàng tháng")

    def load_daily_revenue(self):
        daily_revenue = self.controller.get_daily_revenue()
        self.daily_revenue_table.setRowCount(len(daily_revenue))

        for row, data in enumerate(daily_revenue):
            self.daily_revenue_table.setItem(row, 0, QTableWidgetItem(data[0].strftime("%Y-%m-%d")))
            self.daily_revenue_table.setItem(row, 1, QTableWidgetItem(str(data[1])))

        daily_trend = self.controller.get_daily_trend()
        self.daily_trend_table.setRowCount(len(daily_trend))

        for row, data in enumerate(daily_trend):
            self.daily_trend_table.setItem(row, 0, QTableWidgetItem(data[0]))
            self.daily_trend_table.setItem(row, 1, QTableWidgetItem(str(data[1])))
            self.daily_trend_table.setItem(row, 2, QTableWidgetItem(str(data[2])))

    def load_weekly_revenue(self):
        weekly_revenue = self.controller.get_weekly_revenue()
        self.weekly_revenue_table.setRowCount(len(weekly_revenue))

        for row, data in enumerate(weekly_revenue):
            self.weekly_revenue_table.setItem(row, 0, QTableWidgetItem(str(data[0])))
            self.weekly_revenue_table.setItem(row, 1, QTableWidgetItem(str(data[1])))
            self.weekly_revenue_table.setItem(row, 2, QTableWidgetItem(str(data[2])))

        weekly_trend = self.controller.get_weekly_trend()
        self.weekly_trend_table.setRowCount(len(weekly_trend))

        for row, data in enumerate(weekly_trend):
            self.weekly_trend_table.setItem(row, 0, QTableWidgetItem(data[0]))
            self.weekly_trend_table.setItem(row, 1, QTableWidgetItem(str(data[1])))
            self.weekly_trend_table.setItem(row, 2, QTableWidgetItem(str(data[2])))

    def load_monthly_revenue(self):
        monthly_revenue = self.controller.get_monthly_revenue()
        self.monthly_revenue_table.setRowCount(len(monthly_revenue))

        for row, data in enumerate(monthly_revenue):
            self.monthly_revenue_table.setItem(row, 0, QTableWidgetItem(str(data[0])))
            self.monthly_revenue_table.setItem(row, 1, QTableWidgetItem(str(data[1])))
            self.monthly_revenue_table.setItem(row, 2, QTableWidgetItem(str(data[2])))

        monthly_trend = self.controller.get_monthly_trend()
        self.monthly_trend_table.setRowCount(len(monthly_trend))

        for row, data in enumerate(monthly_trend):
            self.monthly_trend_table.setItem(row, 0, QTableWidgetItem(data[0]))
            self.monthly_trend_table.setItem(row, 1, QTableWidgetItem(str(data[1])))
            self.monthly_trend_table.setItem(row, 2, QTableWidgetItem(str(data[2])))

# Chạy ứng dụng
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ReportView()
    window.show()
    sys.exit(app.exec())
