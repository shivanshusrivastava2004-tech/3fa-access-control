"""
password_auth.py
Factor 2: Password verification.
Passwords are never stored in plaintext -- only salted SHA-256 hashes are
persisted, per OWASP guidance on credential storage.
"""

import hashlib
import json
import os
import secrets

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "credentials.json")


def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def load_credentials() -> dict:
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    with open(CREDENTIALS_FILE, "r") as f:
        return json.load(f)


def register_password(username: str, password: str):
    """Registers a new user with a salted password hash."""
    credentials = load_credentials()
    salt = secrets.token_hex(16)
    credentials[username] = {
        "salt": salt,
        "hash": _hash_password(password, salt),
    }
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(credentials, f, indent=2)
    print(f"Password registered for user '{username}'.")


def verify_password(username: str, password: str) -> bool:
    """Checks a plaintext password attempt against the stored salted hash."""
    credentials = load_credentials()
    record = credentials.get(username)
    if not record:
        return False
    attempt_hash = _hash_password(password, record["salt"])
    return secrets.compare_digest(attempt_hash, record["hash"])
