import unittest
from shop.report import format_price
class T(unittest.TestCase):
    def test_cents(self):
        self.assertEqual(format_price(12.5), "$12.50")
        self.assertEqual(format_price(3), "$3.00")
        self.assertEqual(format_price(0.07), "$0.07")
