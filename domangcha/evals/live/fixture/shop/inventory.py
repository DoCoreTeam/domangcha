class Inventory:
    def __init__(self, stock=None):
        self.stock = dict(stock or {})

    def reserve(self, name, qty):
        self.stock[name] = self.stock.get(name, 0) - qty
        return self.stock[name]
