"""
face_auth.py
Factor 3: Facial recognition verification using OpenCV + face_recognition.
Compares a live webcam/ESP32-CAM frame against enrolled face encodings.
"""

import os
import pickle

import cv2
import face_recognition

ENCODINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "face_encodings.pkl")

# Distance threshold below which two faces are considered a match.
# Lower = stricter (fewer false accepts, more false rejects).
MATCH_TOLERANCE = 0.45


def load_known_encodings() -> dict:
    if not os.path.exists(ENCODINGS_FILE):
        return {}
    with open(ENCODINGS_FILE, "rb") as f:
        return pickle.load(f)


def save_known_encodings(encodings: dict):
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(encodings, f)


def enroll_face_from_camera(username: str, camera_index: int = 0):
    """Captures a frame from the camera and stores the face encoding for a user."""
    cap = cv2.VideoCapture(camera_index)
    print("Look at the camera. Press SPACE to capture, ESC to cancel.")

    encoding = None
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Enroll Face - press SPACE", frame)
        key = cv2.waitKey(1)

        if key % 256 == 27:  # ESC
            print("Enrollment cancelled.")
            break
        elif key % 256 == 32:  # SPACE
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            if not face_locations:
                print("No face detected, try again.")
                continue
            encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            encoding = encodings[0]
            break

    cap.release()
    cv2.destroyAllWindows()

    if encoding is not None:
        known = load_known_encodings()
        known[username] = encoding
        save_known_encodings(known)
        print(f"Face enrolled for user '{username}'.")
    return encoding


def verify_face(camera_index: int = 0, timeout_frames: int = 60) -> tuple[bool, str | None]:
    """Captures live frames and checks them against enrolled encodings.

    Returns (True, username) on a confident match within timeout_frames,
    otherwise (False, None).
    """
    known = load_known_encodings()
    if not known:
        print("No enrolled faces found. Run enroll_face.py first.")
        return False, None

    known_names = list(known.keys())
    known_encodings = list(known.values())

    cap = cv2.VideoCapture(camera_index)
    frames_checked = 0
    result = (False, None)

    while frames_checked < timeout_frames:
        ret, frame = cap.read()
        if not ret:
            continue
        frames_checked += 1

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = distances.argmin() if len(distances) else None

            if best_match_index is not None and distances[best_match_index] < MATCH_TOLERANCE:
                result = (True, known_names[best_match_index])
                break

        if result[0]:
            break

    cap.release()
    return result
