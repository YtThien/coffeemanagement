class CartModel:
    def __init__(self):
        self.cart_items = []

    def add_item(self, name, price):
        for item in self.cart_items:
            if item['name'] == name:
                item['quantity'] += 1
                item['total_price'] = item['quantity'] * item['price']
                return
        self.cart_items.append({'name': name, 'price': price, 'quantity': 1, 'total_price': price})

    def remove_item(self, index):
        if 0 <= index < len(self.cart_items):
            del self.cart_items[index]

    def update_item_quantity(self, index, quantity):
        if 0 <= index < len(self.cart_items):
            self.cart_items[index]['quantity'] = quantity
            self.cart_items[index]['total_price'] = quantity * self.cart_items[index]['price']

    def clear_cart(self):
        self.cart_items = []

    def get_items(self):
        return self.cart_items

    def calculate_total_amount(self):
        total_amount = sum(item['total_price'] for item in self.cart_items)
        return total_amount

    def get_item_by_index(self, index):
        if 0 <= index < len(self.cart_items):
            return self.cart_items[index]
        return None

    def get_item_count(self):
        return len(self.cart_items)

    def get_total_price_by_name(self, name):
        for item in self.cart_items:
            if item['name'] == name:
                return item['total_price']
        return 0
