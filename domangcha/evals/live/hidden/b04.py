import unittest
from shop.cart import Cart
class T(unittest.TestCase):
    def test_once(self):
        c = Cart(); c.add("pen", 100.0)
        c.apply_coupon("SAVE10", 10); c.apply_coupon("SAVE10", 10)
        self.assertEqual(c.total(), 90.0)
    def test_two_codes(self):
        c = Cart(); c.add("pen", 100.0)
        c.apply_coupon("A", 10); c.apply_coupon("B", 10)
        self.assertEqual(c.total(), 81.0)
