class Bill:
    def __init__(self, id, id_customer, id_staff, date, total):
        self.id = id
        self.id_customer = id_customer
        self.id_staff = id_staff
        self.date = date
        self.total = total

    def __repr__(self):
        return f"Bill({self.id}, {self.id_customer}, {self.id_staff}, {self.date}, {self.total})"

class BillDetail:
    def __init__(self, menu_name, quantity, price):
        self.menu_name = menu_name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"BillDetail(menu_name={self.menu_name}, quantity={self.quantity}, price={self.price})"