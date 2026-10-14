import unittest
from shop.inventory import Inventory
class T(unittest.TestCase):
    def test_restock(self):
        inv = Inventory({"pen": 1}); inv.restock("pen", 4); inv.restock("cup", 2)
        self.assertEqual(inv.stock, {"pen": 5, "cup": 2})
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                inv.restock("pen", bad)
