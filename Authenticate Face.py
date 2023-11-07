import cv2
import sqlite3
import numpy as np
import pickle
import serial
# port = serial.Serial('COM5',9600)
conn = sqlite3.connect('face_data.db')
cursor = conn.cursor()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

confidence_threshold = 25

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]

        face = cv2.resize(face, (100, 100))

        face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        cursor.execute("SELECT id, face_data FROM faces")
        rows = cursor.fetchall()

        for row in rows:
            stored_id, stored_face_data = row
            stored_face_data = np.frombuffer(stored_face_data, dtype=np.uint8)
            stored_face = cv2.imdecode(stored_face_data, cv2.IMREAD_GRAYSCALE)

            stored_face = cv2.resize(stored_face, (100, 100))

            diff = cv2.absdiff(stored_face, face_gray)

            if np.mean(diff) < confidence_threshold:
                print("Face Matched with high accuracy!")
                # port.write(str.encode('1'))
                break
        else:
            print("No matching face found")
            # port.write(str.encode('0'))

        cv2.imshow('Captured Face', face)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


conn.close()
