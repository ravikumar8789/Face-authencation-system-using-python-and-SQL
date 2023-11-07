import cv2
import sqlite3
import numpy as np

conn = sqlite3.connect('face_data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS faces
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                face_data BLOB)''')
conn.commit()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

face_count = 0
max_faces = 5

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]

        face = cv2.resize(face, (100, 100))

        face_data = cv2.imencode('.jpg', face)[1].tobytes()

        cursor.execute("INSERT INTO faces (face_data) VALUES (?)", (sqlite3.Binary(face_data),))
        conn.commit()

        face_count += 1

    cv2.imshow('Face Detection', frame)

    if face_count >= max_faces:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

conn.close()
