import unittest
from shop.inventory import Inventory
class T(unittest.TestCase):
    def test_low(self):
        inv = Inventory({"pen": 1, "cup": 5, "bag": 0})
        self.assertEqual(inv.low_stock(2), ["bag", "pen"])
