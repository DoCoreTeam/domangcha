import unittest
from shop.cart import Cart
class T(unittest.TestCase):
    def test_remove(self):
        c = Cart(); c.add("pen", 2.0, 2); c.add("cup", 1.0); c.remove("pen")
        self.assertEqual(c.total(), 1.0)
        with self.assertRaises(KeyError):
            c.remove("nope")
