import json, shutil, tempfile, unittest
from pathlib import Path
from shop import users
class T(unittest.TestCase):
    def setUp(self):
        self.backup = users.DATA.read_text()
    def tearDown(self):
        users.DATA.write_text(self.backup)
    def test_deactivate(self):
        users.deactivate(2)
        saved = {u["id"]: u for u in json.loads(users.DATA.read_text())}
        self.assertFalse(saved[2]["active"]); self.assertTrue(saved[1]["active"])
        with self.assertRaises(KeyError):
            users.deactivate(99)
