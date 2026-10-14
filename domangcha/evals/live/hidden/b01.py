import unittest
from shop.cart import Cart
class T(unittest.TestCase):
    def test_qty(self):
        c = Cart(); c.add("pen", 2.0, 3); c.add("cup", 5.0)
        self.assertEqual(c.total(), 11.0)
