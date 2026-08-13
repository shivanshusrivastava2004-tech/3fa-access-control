# 3-Factor Authentication Access Control System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-Uno-00979D.svg)](https://www.arduino.cc/)
[![OpenCV](https://img.shields.io/badge/OpenCV-FaceRecognition-5C3EE8.svg)](https://opencv.org/)


A hardware-integrated **multi-layer authentication system** combining RFID, password verification, and real-time facial recognition — achieving **0% False Acceptance Rate** and **94% True Positive Rate**.

---

## 🎯 Overview

Single-factor authentication is a single point of failure. This project implements a layered, 3-factor access control pipeline where a user must pass **all three checks** — something they *have* (RFID card), something they *know* (password), and something they *are* (face) — before access is granted, with an ESP32-CAM / Arduino-driven servo lock as the physical actuator.

## 🏗️ System Architecture

```
   ┌──────────────┐      ┌───────────────┐      ┌────────────────────┐
   │  RFID Scan   │ ---> │   Password     │ ---> │  Facial Recognition │
   │ (Factor 1)   │      │  (Factor 2)    │      │     (Factor 3)      │
   └──────────────┘      └───────────────┘      └────────────────────┘
                                                            │
                                                            ▼
                                              ┌───────────────────────────┐
                                              │  Python Backend Decision   │
                                              │  Engine (Serial Comm)      │
                                              └───────────────────────────┘
                                                            │
                                                            ▼
                                              ┌───────────────────────────┐
                                              │  Arduino → Servo Lock      │
                                              │  (Grant / Deny Access)     │
                                              └───────────────────────────┘
```

## ✨ Features

- **RFID Verification** — First-layer identity check via RFID tag/card
- **Password Authentication** — Secondary knowledge-based factor
- **Real-Time Facial Recognition** — OpenCV + `face_recognition` library for biometric verification
- **Serial Communication** — Python backend ↔ Arduino hardware for real-time decisioning
- **Physical Access Control** — Servo-driven lock mechanism triggered on successful 3-factor match
- **Security Hardening** — Applied OWASP Top 10 principles to protect against common vulnerabilities

## 📊 Performance

| Metric | Result |
|---|---|
| False Acceptance Rate (FAR) | **0%** |
| True Positive Rate (TPR) | **94%** |

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Facial Recognition | Python, OpenCV, `face_recognition` |
| Hardware | Arduino Uno, ESP32-CAM, RFID module, Servo motor, PIR sensor |
| Communication | Serial (USB/UART) |
| Security | OWASP Top 10 practices |

## 📦 Hardware Requirements

- Arduino Uno
- ESP32-CAM module
- RFID reader (RC522) + tags
- Servo motor (lock actuator)
- PIR motion sensor
- Jumper wires, breadboard, 5V power supply

## 💻 Software Installation

```bash
git clone https://github.com/<your-username>/3fa-access-control.git
cd 3fa-access-control
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Setup

1. Flash `arduino/lock_controller.ino` to your Arduino Uno via the Arduino IDE.
2. Wire the RFID module, servo, and PIR sensor per `docs/circuit_diagram.png`.
3. Register authorized faces:
   ```bash
   python src/enroll_face.py --name "user1"
   ```
4. Run the authentication system:
   ```bash
   python src/main.py --port /dev/ttyUSB0   # or COM3 on Windows
   ```

## 📁 Project Structure

```
3fa-access-control/
├── src/
│   ├── main.py              # Orchestrates the 3-factor auth flow
│   ├── rfid_auth.py         # RFID verification logic
│   ├── password_auth.py     # Password check module
│   ├── face_auth.py         # Facial recognition verification
│   └── enroll_face.py       # Registers new authorized faces
├── arduino/
│   └── lock_controller.ino  # Servo lock + PIR sensor firmware
├── docs/
│   └── circuit_diagram.png
├── assets/
│   └── demo.gif
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔒 Security Considerations

Applied OWASP Top 10 guidelines to harden the system, including secure credential storage, input validation, and protection against replay/spoofing attempts on the backend communication layer.


## 👤 Author

**Shivanshu Srivastava**
[LinkedIn](https://www.linkedin.com/in/shivanshu-srivastava-19840728b/) · shivanshu.srivastava2004@gmail.com
