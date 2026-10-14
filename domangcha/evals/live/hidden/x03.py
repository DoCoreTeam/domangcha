import unittest
from shop.users import find_by_email
class T(unittest.TestCase):
    def test_case(self):
        self.assertEqual(find_by_email("ada@EXAMPLE.com")["id"], 1)
        self.assertEqual(find_by_email("BOB@example.com")["id"], 2)
        self.assertIsNone(find_by_email("zed@example.com"))
