import unittest

from shop.cart import Cart
from shop.inventory import Inventory
from shop.users import find_by_email, is_admin


class BasicTests(unittest.TestCase):
    def test_single_item_total(self):
        cart = Cart()
        cart.add("pen", 3.0)
        self.assertEqual(cart.total(), 3.0)

    def test_reserve_reduces_stock(self):
        self.assertEqual(Inventory({"pen": 5}).reserve("pen", 2), 3)

    def test_admin_lookup(self):
        self.assertTrue(is_admin(find_by_email("Ada@example.com")))


if __name__ == "__main__":
    unittest.main()
