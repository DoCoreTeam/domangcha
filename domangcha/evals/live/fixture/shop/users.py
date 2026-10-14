import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "users.json"


def load():
    return json.loads(DATA.read_text())


def save(users):
    DATA.write_text(json.dumps(users, indent=2) + "\n")


def find_by_email(email):
    for user in load():
        if user["email"] == email:
            return user
    return None


def is_admin(user):
    return user.get("role") == "admin"
