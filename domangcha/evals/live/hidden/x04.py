import unittest
from shop.report import format_price
class T(unittest.TestCase):
    def test_negative(self):
        self.assertEqual(format_price(-5), "($5.00)")
        self.assertEqual(format_price(5), "$5.00")
