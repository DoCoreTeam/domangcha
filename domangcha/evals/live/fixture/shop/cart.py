class Cart:
    def __init__(self):
        self.items = {}
        self.coupons = []

    def add(self, name, price, qty=1):
        if name in self.items:
            self.items[name]["qty"] += qty
        else:
            self.items[name] = {"price": price, "qty": qty}

    def apply_coupon(self, code, percent):
        self.coupons.append((code, percent))

    def total(self):
        subtotal = sum(item["price"] for item in self.items.values())
        for _code, percent in self.coupons:
            subtotal = subtotal * (100 - percent) / 100
        return round(subtotal, 2)
