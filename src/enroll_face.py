"""
enroll_face.py
CLI utility to register a new authorized user's face, RFID UID, and password
all in one step.
"""

import argparse

from face_auth import enroll_face_from_camera
from rfid_auth import register_uid
from password_auth import register_password


def main():
    parser = argparse.ArgumentParser(description="Enroll a new authorized user.")
    parser.add_argument("--name", type=str, required=True, help="Username to register.")
    parser.add_argument("--uid", type=str, help="RFID card UID (optional, can register later).")
    parser.add_argument("--password", type=str, help="Password (optional, can register later).")
    parser.add_argument("--camera-index", type=int, default=0)
    args = parser.parse_args()

    print(f"Enrolling user: {args.name}")
    enroll_face_from_camera(args.name, camera_index=args.camera_index)

    if args.uid:
        register_uid(args.uid, args.name)
    if args.password:
        register_password(args.name, args.password)

    print("Enrollment complete.")


if __name__ == "__main__":
    main()
