import cv2
import numpy as np
import sqlite3

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Set the resolution
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Database setup
conn = sqlite3.connect('face_recognition.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (name TEXT, age INTEGER, email TEXT, face_image BLOB)''')
conn.commit()

# List to hold known face images and their corresponding names
known_face_images = []
known_face_names = []
recognizer = cv2.face.LBPHFaceRecognizer_create()  # Create LBPH face recognizer


# Load stored faces from the database at startup
def load_registered_faces():
    global known_face_images, known_face_names
    c.execute("SELECT name, face_image FROM users")
    rows = c.fetchall()
    for row in rows:
        name, face_image_blob = row
        face_image = np.frombuffer(face_image_blob, dtype=np.uint8)
        face_image = face_image.reshape((100, 100))  # Adjust shape as per saved dimensions
        known_face_images.append(face_image)
        known_face_names.append(name)

    # Train recognizer if there are known faces
    if known_face_images:
        labels = np.array(range(len(known_face_names)))
        recognizer.train(known_face_images, labels)


# Register a new face
def register_face(name, age, email):
    global known_face_images, known_face_names
    # Capture a single frame from the video
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame for registration")
        return

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using OpenCV's Haar cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    # Loop through detected faces and register the first detected one
    for (x, y, w, h) in faces:
        face_image = gray_frame[y:y + h, x:x + w]
        face_image_resized = cv2.resize(face_image, (100, 100))  # Resize to a fixed size
        known_face_images.append(face_image_resized)
        known_face_names.append(name)

        # Store the face image and user details in the database
        c.execute("INSERT INTO users (name, age, email, face_image) VALUES (?, ?, ?, ?)",
                  (name, age, email, face_image_resized.tobytes()))
        conn.commit()

        print(f"Registered {name} successfully!")

        # Train the recognizer with the updated list of known faces
        if known_face_images:
            labels = np.array(range(len(known_face_names)))
            recognizer.train(known_face_images, labels)
        break  # Register only the first detected face


# Load previously registered faces
load_registered_faces()

# Input states
input_stage = 0  # 0: Name, 1: Age, 2: Email
name_input = ""
age_input = ""
email_input = ""

while True:
    # Capture a frame from the video
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Extract the face region
        face_image = gray_frame[y:y + h, x:x + w]
        face_image_resized = cv2.resize(face_image, (100, 100))  # Resize to match training data

        # Check if there are known faces registered before predicting
        if known_face_images:
            id_, confidence = recognizer.predict(face_image_resized)
            if confidence < 100:
                name = known_face_names[id_]  # Get the name from the list
            else:
                name = "Unknown"
        else:
            name = "Unknown"  # No known faces registered

        # Draw a rectangle around the face and put the name
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the input fields on the frame
    cv2.putText(frame, f"Name: {name_input}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Age: {age_input}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Email: {email_input}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show the resulting frame
    cv2.imshow('Video', frame)

    # Key press logic
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # Enter key
        if input_stage == 0:  # Name input stage
            input_stage = 1  # Move to age input stage
        elif input_stage == 1:  # Age input stage
            input_stage = 2  # Move to email input stage
        elif input_stage == 2:  # Email input stage
            if name_input and age_input.isdigit() and email_input:  # Check if the inputs are valid
                register_face(name_input, int(age_input), email_input)
                name_input, age_input, email_input = "", "", ""  # Clear inputs after registration
                input_stage = 0  # Reset to name input stage
    elif key == 27:  # Esc key to exit
        break
    elif key >= 32 and key <= 126:  # Printable ASCII characters
        if input_stage == 0:  # Inputting name
            name_input += chr(key)
        elif input_stage == 1:  # Inputting age
            age_input += chr(key)
        elif input_stage == 2:  # Inputting email
            email_input += chr(key)
    elif key == 8:  # Backspace to remove the last character
        if input_stage == 2 and email_input:
            email_input = email_input[:-1]
        elif input_stage == 1 and age_input:
            age_input = age_input[:-1]
        elif input_stage == 0 and name_input:
            name_input = name_input[:-1]

# Release the video capture and destroy windows properly
video_capture.release()
conn.close()  # Close the database connection
cv2.destroyAllWindows()