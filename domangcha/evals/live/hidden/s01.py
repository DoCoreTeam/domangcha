import unittest
from shop.users import is_admin
class T(unittest.TestCase):
    def test_case(self):
        for role in ("admin", "Admin", "ADMIN"):
            self.assertTrue(is_admin({"role": role}))
        for role in ("user", "", None):
            self.assertFalse(is_admin({"role": role}))
        self.assertFalse(is_admin({}))
