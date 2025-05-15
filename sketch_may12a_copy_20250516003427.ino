#include <Servo.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

// LCD I2C
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Ultrasonic Pins
const int trigPin = 12;
const int echoPin = 13;

// Servo Pins
const int servoMainPin = 8;
const int servo180Pin = 9;
const int servo2Pin = 10;
const int servo3Pin = 11;

// LED Pin
const int ledPin = 2;

// Keypad setup
const byte ROWS = 1;
const byte COLS = 3;

char keys[ROWS][COLS] = {
  {'b', 'c', 'd'}
};

byte rowPins[ROWS] = {6};
byte colPins[COLS] = {3, 4, 5};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// Objects
Servo servoMain;
Servo servo180;
Servo servo2;
Servo servo3;

// State variables
bool hasRotated = false;
bool servo2Running = false;
bool servo3Running = false;

long duration;
float distance;

String inputPassword = "";
const String correctPassword = "bcd";

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);

  servoMain.attach(servoMainPin);
  servo180.attach(servo180Pin);
  servo2.attach(servo2Pin);
  servo3.attach(servo3Pin);

  servoMain.write(90);
  servo180.write(180);
  servo2.write(90);
  servo3.write(90);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(2, 0);
  lcd.print("Enter Password");

  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    inputPassword += key;

    lcd.setCursor(0, 1);
    for (int i = 0; i < inputPassword.length(); i++) {
      lcd.print("*");
    }

    if (inputPassword.length() == 3) {
      delay(500);
      lcd.clear();
      if (inputPassword == correctPassword) {
        lcd.setCursor(0, 0);
        lcd.print("Access Granted");
        rotateServoMultipleTurns(servoMain, 180);
      } else {
        lcd.setCursor(0, 0);
        lcd.print("Access Denied");
      }
      delay(2000);
      inputPassword = "";   
      lcd.clear();
      lcd.setCursor(2, 0);
      lcd.print("Enter Password");
    }
  }

  if (Serial.available()) {
    char input = Serial.read();

    switch (input) {
      case '9':
        rotateServoMultipleTurns(servoMain, 180);
        break;
      case '1':
        servo2Running = true;
        break;
      case '2':
        servo2Running = false;
        servo2.write(90);
        break;
      case '3':
        servo180.write(180);  
        break;
      case '4':
        servo180.write(0);    
        break;
      case '7':
        servo3Running = true;
        break;
      case '8':
        servo3Running = false;
        servo3.write(90);
        break;
      case '5':
        digitalWrite(ledPin, HIGH);
        break;
      case '6':
        digitalWrite(ledPin, LOW);
        break;
    }
  }

  if (servo2Running) {
    servo2.write(0);
  }

  if (servo3Running) {
    servo3.write(0);
  }

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  if (distance <= 10 && distance > 0 && !hasRotated) {
    rotateServoMultipleTurns(servoMain, 0);  
    hasRotated = true;
  } else if (distance > 10) {
    hasRotated = false;
    servoMain.write(90);
  }

  delay(100);
}

void rotateServoMultipleTurns(Servo s, int angle) {
  for (int i = 0; i < 4; i++) {
    s.write(angle);
    delay(1000);
    s.write(90);
    delay(200);
  }
}