import unittest
from shop.cart import Cart
from shop.report import to_csv
class T(unittest.TestCase):
    def test_csv(self):
        c = Cart(); c.add("pen", 2.5, 2); c.add("cup", 1.0)
        lines = [l.strip() for l in to_csv(c).strip().splitlines()]
        self.assertEqual(lines, ["name,price,qty", "cup,1.0,1", "pen,2.5,2"])
