"""
main.py
Orchestrates the full 3-factor authentication flow:
RFID -> Password -> Facial Recognition -> unlock signal to Arduino.

All three factors must pass before an "UNLOCK" command is sent over serial.
"""

import argparse
import time

import serial

from rfid_auth import verify_rfid
from password_auth import verify_password
from face_auth import verify_face

BAUD_RATE = 9600


def run_auth_flow(ser: serial.Serial) -> bool:
    print("\n--- Factor 1: RFID ---")
    uid = input("Scan RFID card (enter UID): ").strip()
    rfid_ok, username = verify_rfid(uid)
    if not rfid_ok:
        print("❌ RFID verification failed.")
        return False
    print(f"✅ RFID verified for user '{username}'.")

    print("\n--- Factor 2: Password ---")
    password = input(f"Enter password for '{username}': ").strip()
    if not verify_password(username, password):
        print("❌ Password verification failed.")
        return False
    print("✅ Password verified.")

    print("\n--- Factor 3: Facial Recognition ---")
    print("Look at the camera...")
    face_ok, matched_name = verify_face()
    if not face_ok or matched_name != username:
        print("❌ Facial recognition failed or does not match RFID/password identity.")
        return False
    print(f"✅ Face verified for user '{username}'.")

    return True


def send_unlock_signal(ser: serial.Serial):
    ser.write(b"UNLOCK\n")
    print("🔓 Unlock signal sent to Arduino.")


def main():
    parser = argparse.ArgumentParser(description="Run the 3-factor authentication system.")
    parser.add_argument("--port", type=str, required=True, help="Serial port, e.g. /dev/ttyUSB0 or COM3")
    parser.add_argument("--baud", type=int, default=BAUD_RATE)
    args = parser.parse_args()

    ser = serial.Serial(args.port, args.baud, timeout=1)
    time.sleep(2)  # allow Arduino to reset after serial connection opens

    print("=== 3-Factor Authentication System ===")
    try:
        while True:
            input("\nPress Enter to start an authentication attempt (Ctrl+C to quit)...")
            success = run_auth_flow(ser)
            if success:
                print("\n✅ ACCESS GRANTED")
                send_unlock_signal(ser)
            else:
                print("\n🚫 ACCESS DENIED")
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
