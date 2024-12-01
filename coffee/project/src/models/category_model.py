class Category:
    def __init__(self, id, name_category, description):
        self.id = id
        self.name_category = name_category
        self.description = description

    def __repr__(self):
        return f"Category({self.id},{self.name_category},{self.description})"
