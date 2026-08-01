/*
  lock_controller.ino
  Runs on Arduino Uno. Listens for an "UNLOCK" command over serial from the
  Python backend, drives a servo to open the physical lock, and uses a PIR
  sensor to auto re-lock after the area is clear.
*/

#include <Servo.h>

Servo lockServo;

const int SERVO_PIN = 9;
const int PIR_PIN = 2;
const int LOCKED_ANGLE = 0;
const int UNLOCKED_ANGLE = 90;
const unsigned long UNLOCK_DURATION_MS = 5000;

String incomingCommand = "";
bool isUnlocked = false;
unsigned long unlockTimestamp = 0;

void setup() {
  Serial.begin(9600);
  lockServo.attach(SERVO_PIN);
  pinMode(PIR_PIN, INPUT);
  lockServo.write(LOCKED_ANGLE);
  Serial.println("READY");
}

void loop() {
  // Read commands from Python backend
  while (Serial.available() > 0) {
    char incomingChar = Serial.read();
    if (incomingChar == '\n') {
      incomingCommand.trim();
      if (incomingCommand == "UNLOCK") {
        unlock();
      }
      incomingCommand = "";
    } else {
      incomingCommand += incomingChar;
    }
  }

  // Auto re-lock after UNLOCK_DURATION_MS, unless PIR still detects presence
  if (isUnlocked && millis() - unlockTimestamp > UNLOCK_DURATION_MS) {
    int motionDetected = digitalRead(PIR_PIN);
    if (motionDetected == LOW) {
      lock();
    } else {
      // Someone's still there — extend the window
      unlockTimestamp = millis();
    }
  }
}

void unlock() {
  lockServo.write(UNLOCKED_ANGLE);
  isUnlocked = true;
  unlockTimestamp = millis();
  Serial.println("UNLOCKED");
}

void lock() {
  lockServo.write(LOCKED_ANGLE);
  isUnlocked = false;
  Serial.println("LOCKED");
}
