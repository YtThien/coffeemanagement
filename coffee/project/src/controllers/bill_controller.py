from datetime import datetime, timedelta
from database import create_connection
from models.bill_model import Bill, BillDetail

class BillController:
    def __init__(self):
        self.conn = create_connection()

    def get_bills(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM bill")
            bills = []
            for row in cursor.fetchall():
                bill = Bill(row[0], row[1], row[2], row[3], row[4])
                bills.append(bill)
            return bills
        except Exception as e:
            print(f"Lỗi khi lấy danh sách hóa đơn: {e}")
            return []

    def create_bill(self, bill):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO bill (id_customer, id_staff, date, total) VALUES (%s, %s, %s, %s)",
                           (bill.id_customer, bill.id_staff, bill.date, bill.total))
            bill_id = cursor.lastrowid

            for item in bill.items:
                cursor.execute("INSERT INTO bill_detail (id_bill, id_menu, quantity, price) VALUES (%s, %s, %s, %s)",
                               (bill_id, item.id_menu, item.quantity, item.price))

            self.conn.commit()

            bill = self.get_bill_by_id(bill_id)
            return bill
        except Exception as e:
            print(f"Lỗi khi tạo hóa đơn: {e}")
            self.conn.rollback()
            return None

    def delete_bill(self, bill_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM bill WHERE id = %s", (bill_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Lỗi khi xóa hóa đơn: {e}")
            self.conn.rollback()

    def get_bill_by_id(self, bill_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM bill WHERE id = %s", (bill_id,))
            row = cursor.fetchone()
            if row:
                bill = Bill(row[0], row[1], row[2], row[3], row[4])
                return bill
            else:
                return None
        except Exception as e:
            print(f"Lỗi khi lấy hóa đơn theo ID: {e}")
            return None

    def get_customer_name(self, customer_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM customer WHERE id = %s", (customer_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except Exception as e:
            print(f"Lỗi khi lấy tên khách hàng: {e}")
            return None

    def get_customer_phone(self, customer_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT phone FROM customer WHERE id = %s", (customer_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except Exception as e:
            print(f"Lỗi khi lấy số điện thoại khách hàng: {e}")
            return None

    def get_staff_name(self, staff_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM staff WHERE id = %s", (staff_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except Exception as e:
            print(f"Lỗi khi lấy tên nhân viên: {e}")
            return None

    def get_bill_details(self, bill_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT m.name_menu AS menu_name, bd.quantity, bd.price FROM bill_detail bd INNER JOIN menu m ON bd.id_menu = m.id WHERE bd.id_bill = %s", (bill_id,))
            bill_details = []
            for row in cursor.fetchall():
                bill_detail = BillDetail(row[0], row[1], row[2])
                bill_details.append(bill_detail)
            return bill_details
        except Exception as e:
            print(f"Lỗi khi lấy chi tiết hóa đơn: {e}")
            return []

    def search_bills_by_phone(self, phone_number):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM bill b INNER JOIN customer c ON b.id_customer = c.id WHERE c.phone LIKE %s", (f"%{phone_number}%",))
            bills = []
            for row in cursor.fetchall():
                bill = Bill(row[0], row[1], row[2], row[3], row[4])
                bills.append(bill)
            return bills
        except Exception as e:
            print(f"Lỗi khi tìm kiếm hóa đơn theo số điện thoại: {e}")
            return []

    def get_daily_revenue(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DATE(date) as day, SUM(total) as revenue FROM bill GROUP BY day")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy doanh thu hằng ngày: {e}")
            return []

    def get_weekly_revenue(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT YEAR(date) as year, WEEK(date, 1) as week, SUM(total) as revenue FROM bill GROUP BY year, week")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy doanh thu hằng tuần: {e}")
            return []

    def get_monthly_revenue(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT YEAR(date) as year, MONTH(date) as month, SUM(total) as revenue 
                FROM bill 
                GROUP BY year, month
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy doanh thu hằng tháng: {e}")
            return []

    def get_sales_trends(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT m.name_menu, SUM(bd.quantity) as quantity_sold FROM bill_detail bd INNER JOIN menu m ON bd.id_menu = m.id GROUP BY m.name_menu ORDER BY quantity_sold DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy xu hướng bán hàng: {e}")
            return []

    def get_daily_trend(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.name_menu, SUM(bd.quantity) as total_quantity, SUM(bd.price * bd.quantity) as total_price
                FROM bill_detail bd
                JOIN menu m ON bd.id_menu = m.id
                JOIN bill b ON bd.id_bill = b.id
                WHERE DATE(b.date) = CURDATE()
                GROUP BY m.name_menu
                ORDER BY total_quantity DESC
            """)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Lỗi khi lấy xu hướng bán hàng hằng ngày: {e}")
            return []

    def get_weekly_trend(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.name_menu, SUM(bd.quantity) as total_quantity, SUM(bd.price * bd.quantity) as total_price
                FROM bill_detail bd
                JOIN menu m ON bd.id_menu = m.id
                JOIN bill b ON bd.id_bill = b.id
                WHERE YEARWEEK(b.date, 1) = YEARWEEK(CURDATE(), 1)
                GROUP BY m.name_menu
                ORDER BY total_quantity DESC
            """)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Lỗi khi lấy xu hướng bán hàng hằng tuần: {e}")
            return []

    def get_monthly_trend(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.name_menu, SUM(bd.quantity) as total_quantity, SUM(bd.price * bd.quantity) as total_price
                FROM bill_detail bd
                JOIN menu m ON bd.id_menu = m.id
                JOIN bill b ON bd.id_bill = b.id
                WHERE MONTH(b.date) = MONTH(CURDATE()) AND YEAR(b.date) = YEAR(CURDATE())
                GROUP BY bd.id_menu
                ORDER BY total_quantity DESC
            """)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Lỗi khi lấy xu hướng bán hàng hằng tháng: {e}")
            return []

    def get_daily_trend_by_date(self, date):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.name_menu, SUM(bd.quantity) as total_quantity, SUM(bd.price * bd.quantity) as total_price
                FROM bill_detail bd
                JOIN menu m ON bd.id_menu = m.id
                JOIN bill b ON bd.id_bill = b.id
                WHERE DATE(b.date) = %s
                GROUP BY bd.id_menu
                ORDER BY total_quantity DESC
            """, (date,))
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Lỗi khi lấy xu hướng bán hàng cho ngày cụ thể: {e}")
            return []

    def get_weekly_trend_by_week(self, year, week):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.name_menu, SUM(bd.quantity) as total_quantity, SUM(bd.price * bd.quantity) as total_price
                FROM bill_detail bd
                JOIN menu m ON bd.id_menu = m.id
                JOIN bill b ON bd.id_bill = b.id
                WHERE YEARWEEK(b.date, 1) = %s
                GROUP BY bd.id_menu
                ORDER BY total_quantity DESC
            """, ((year, week),))
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Lỗi khi lấy xu hướng bán hàng cho tuần cụ thể: {e}")
            return []

    def get_monthly_trend_by_month(self, year, month):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.name_menu, SUM(bd.quantity) as total_quantity, SUM(bd.price * bd.quantity) as total_price
                FROM bill_detail bd
                JOIN menu m ON bd.id_menu = m.id
                JOIN bill b ON bd.id_bill = b.id
                WHERE MONTH(b.date) = %s AND YEAR(b.date) = %s
                GROUP BY bd.id_menu
                ORDER BY total_quantity DESC
            """, (month, year))
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Lỗi khi lấy xu hướng bán hàng cho tháng cụ thể: {e}")
            return []