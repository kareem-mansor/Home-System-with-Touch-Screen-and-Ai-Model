
# 🏠 Smart Home Automation System with Touch Screen & Face Recognition

This project is a modern home automation system built using Arduino and Python. It features control over multiple rooms, garage, and main door, integrating sensors, servo motors, touch screens, and face recognition technology.

---

## 📌 Features

- ✅ Two bedrooms with:
  - 360° servo motors acting as fans
  - LED lights
- 🚪 Main door access using:
  - Face recognition (via Python + OpenCV)
  - 180° servo motor
  - 4x4 keypad as alternative input
- 🚗 Garage automation:
  - Ultrasonic sensor detects car presence
  - 360° servo motor to open/close the door
- 🖥️ Two touchscreen interfaces:
  - Outdoor: Choose to ring doorbell or scan face
  - Indoor: Control all house devices (lights, fans, door, garage)
- 📲 Mobile control via QR code and open-source web link
- 📟 LCD (I2C) to display system status

---

## 🧠 System Architecture

- **Arduino Uno** for hardware control
- **Python + OpenCV** for face recognition
- **Serial communication** between Python and Arduino
- **Servo motors (180°/360°)** for movement control
- **Ultrasonic sensor** for garage automation
- **Touch screens** for UI
- **Mobile device access** via QR link

---

## 🔧 Technologies Used

- Arduino (C++)
- Python 3
- OpenCV (Face Recognition)
- Touch screen GUI library
- LCD (I2C)
- Keypad 4x4
- Servo motors
- Ultrasonic sensor
- QR Code generation (for mobile access)

---

## 🧪 Testing

- ✅ Unit testing for sensors, motors, and modules
- ✅ Integration testing for full system functionality
- ✅ Simulated use cases:
  - Face detection opens door
  - Garage closes on car detection
  - Mobile phone interface sends commands

---

## 🚀 Future Improvements

- Integration with voice assistants (e.g., Alexa or Google Assistant)
- Replace Arduino Uno with ESP32 (WiFi built-in)
- Add real-time camera streaming
- Push notifications on mobile app
- Enhanced mobile app UI

---

## 📷 Demo

> _Insert image or link to video demo here_

---

## 📁 Folder Structure

```
project-root/
│
├── ArduinoCode/
│   └── home_automation.ino
├── PythonFaceRecognition/
│   └── face_recognition.py
├── TouchScreenGUI/
│   └── gui_code.ino
├── QR_Link/
│   └── qr_code.png
├── images/
│   └── system_diagram.png
├── README.md
```

