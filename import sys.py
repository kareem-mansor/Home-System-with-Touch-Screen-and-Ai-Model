import sys
import serial
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QFrame, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# فتح الاتصال مع Arduino (تأكد من صحة المنفذ)
arduino = serial.Serial('COM4', 9600)
time.sleep(2)  # انتظار بسيط لتهيئة الاتصال

class RoomGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Home Layout")
        self.setGeometry(200, 200, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(30)

        common_color = "#D6EAF8"

        # Room 1
        room1_frame = self.create_room("Room 1", [
            "💡 Open Light",
            "❌💡 Closed Light",
            "🌀 Open Fan1",
            "❌🌀 Closed Fan1",
            
        ], common_color)
        layout.addWidget(room1_frame, 0, 0)

        # Room 2
        room2_frame = self.create_room("Room 2", [
            "💡 Open Light",
            "❌💡 Closed Light",
            "🌀 Open Fan",
            "❌🌀 Closed Fan",
            
        ], common_color)
        layout.addWidget(room2_frame, 0, 1)

        # Garage
        garage_frame = self.create_room("Garage", [
            "🚗 Open Garage",
            "❌🚗 Closed Garage",
            "💡 Open Light",
            "❌💡 Closed Light",
          
        ], common_color)
        layout.addWidget(garage_frame, 1, 0)

        # Living Room
        living_frame = self.create_room("Living Room", [
            "🚪 Open Door",
            "❌🚪 Closed Door",
            "🚗 Open Garage",
            "❌🚗 Closed Garage"
        ], common_color)
        layout.addWidget(living_frame, 1, 1)

        self.setLayout(layout)

    def create_room(self, title, control_texts, bg_color):
        frame = QFrame()
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        title_label.setStyleSheet("color: #2980B9;")
        layout.addWidget(title_label)

        for text in control_texts:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(f"""
                background-color: {bg_color};
                border: 2px solid #16A085;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                color: #1A5276;
            """)

            if "Light" in text:
                button.clicked.connect(lambda _, t=text: self.handle_light_click(t))
            elif "Fan1" in text or "Fan" in text:
                button.clicked.connect(lambda _, t=text: self.handle_fan_click(t))
            elif "Garage" in text:
                button.clicked.connect(lambda _, t=text: self.handle_garage_click(t))
            elif "Door" in text:
                button.clicked.connect(lambda _, t=text: self.handle_door_click(t))

            layout.addWidget(button)

        frame.setLayout(layout)
        frame.setStyleSheet("""
            QFrame {
                background: linear-gradient(to right, #E8F8F5, #D6EAF8);
                border: 2px solid #1ABC9C;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        return frame

    def handle_light_click(self, text):
        if "Open Light" in text:
            arduino.write(b'5\n')
        elif "Closed Light" in text:
            arduino.write(b'6\n')

    def handle_fan_click(self, text):
        if "Open Fan1" in text:
            arduino.write(b'1\n')
        elif "Closed Fan1" in text:
            arduino.write(b'2\n')
        elif "Open Fan" in text:
            arduino.write(b'7\n')
        elif "Closed Fan" in text:
            arduino.write(b'8\n')

    def handle_garage_click(self, text):
        if "Open Garage" in text:
            arduino.write(b'9\n')
        elif "Closed Garage" in text:
            arduino.write(b'10\n')

    def handle_door_click(self, text):
        if "Open Door" in text:
            arduino.write(b'4\n')
        elif "Closed Door" in text:
            arduino.write(b'3\n')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoomGrid()
    window.show()
    sys.exit(app.exec_())
