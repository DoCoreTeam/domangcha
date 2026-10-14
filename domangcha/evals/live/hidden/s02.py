import unittest
from shop.cart import Cart
from shop.report import summary
class T(unittest.TestCase):
    def test_perm(self):
        c = Cart(); c.add("pen", 1.0)
        self.assertIn("total", summary(c, {"role": "admin"}))
        with self.assertRaises(PermissionError):
            summary(c, {"role": "user"})
