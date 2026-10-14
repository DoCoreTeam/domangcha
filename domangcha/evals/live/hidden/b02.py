import unittest
from shop.inventory import Inventory
class T(unittest.TestCase):
    def test_short(self):
        inv = Inventory({"pen": 1})
        with self.assertRaises(ValueError):
            inv.reserve("pen", 2)
        self.assertEqual(inv.stock["pen"], 1)
    def test_ok(self):
        self.assertEqual(Inventory({"pen": 3}).reserve("pen", 3), 0)
