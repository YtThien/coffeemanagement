class Menu:
    def __init__(self,id,id_category,name_menu,price,description):
        self.id = id
        self.id_category = id_category
        self.name_menu = name_menu
        self.price = price
        self.description = description
    def __repr__(self):
        return f"Menu({self.id},{self.id_category},{self.name_menu},{self.price},{self.description})"