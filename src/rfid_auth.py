"""
rfid_auth.py
Factor 1: RFID card verification.
Listens on the serial connection for a tag UID sent by the Arduino/RFID
reader and checks it against a whitelist of authorized UIDs.
"""

import json
import os

AUTHORIZED_UIDS_FILE = os.path.join(os.path.dirname(__file__), "..", "authorized_uids.json")


def load_authorized_uids() -> dict:
    """Loads the mapping of RFID UID -> username from a local JSON whitelist."""
    if not os.path.exists(AUTHORIZED_UIDS_FILE):
        return {}
    with open(AUTHORIZED_UIDS_FILE, "r") as f:
        return json.load(f)


def verify_rfid(uid: str) -> tuple[bool, str | None]:
    """Checks a scanned UID against the authorized list.

    Returns (True, username) if authorized, else (False, None).
    """
    authorized = load_authorized_uids()
    uid = uid.strip().upper()
    if uid in authorized:
        return True, authorized[uid]
    return False, None


def register_uid(uid: str, username: str):
    """Adds a new UID -> username mapping to the whitelist."""
    authorized = load_authorized_uids()
    authorized[uid.strip().upper()] = username
    with open(AUTHORIZED_UIDS_FILE, "w") as f:
        json.dump(authorized, f, indent=2)
    print(f"Registered UID {uid} for user '{username}'.")
