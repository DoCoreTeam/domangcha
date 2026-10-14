import unittest
from shop.cart import Cart
class T(unittest.TestCase):
    def test_cap(self):
        c = Cart(); c.add("pen", 1.0, 99)
        with self.assertRaises(ValueError):
            c.add("pen", 1.0, 1)
        with self.assertRaises(ValueError):
            Cart().add("cup", 1.0, 100)
