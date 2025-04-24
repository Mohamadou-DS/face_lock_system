import cv2
import face_recognition
import json
import time
import ctypes
from datetime import datetime

def load_known_faces():
    with open("users.json", "r") as f:
        users = json.load(f)

    encodings = []
    names = []
    for user in users:
        image = face_recognition.load_image_file(user["path"])
        encoding = face_recognition.face_encodings(image)[0]
        encodings.append(encoding)
        names.append(user["name"])
    return encodings, names

def lock_windows():
    ctypes.windll.user32.LockWorkStation()

def log_event(event):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} - {event}\n")

def face_detection_loop(interval=3):
    known_encodings, known_names = load_known_faces()
    video = cv2.VideoCapture(0)
    missing_counter = 0

    while True:
        ret, frame = video.read()
        rgb = frame[:, :, ::-1]

        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        recognized = False
        for face_encoding in encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            if True in matches:
                name = known_names[matches.index(True)]
                log_event(f"Utilisateur reconnu : {name}")
                recognized = True
                missing_counter = 0
                break

        if not recognized:
            missing_counter += 1
            log_event("Visage non reconnu.")
            if missing_counter >= 5:
                log_event("Verrouillage du système.")
                lock_windows()
                break

        time.sleep(interval)
