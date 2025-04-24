import sys
import os
import json
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QFileDialog, QLineEdit, QMessageBox
)
from face_lock import face_detection_loop
from auto_start import add_to_startup

class FaceLockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Lock System")
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Nom de l'utilisateur:")
        self.layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.add_button = QPushButton("Ajouter un utilisateur")
        self.add_button.clicked.connect(self.add_user)
        self.layout.addWidget(self.add_button)

        self.start_button = QPushButton("Démarrer la détection")
        self.start_button.clicked.connect(self.start_detection)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def add_user(self):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom.")
            return
        path, _ = QFileDialog.getOpenFileName(self, "Sélectionnez une image")
        if not path:
            return
        os.makedirs("users_faces", exist_ok=True)
        dest_path = os.path.join("users_faces", f"{name}.jpg")
        shutil.copy(path, dest_path)

        if not os.path.exists("users.json"):
            with open("users.json", "w") as f:
                json.dump([], f)

        with open("users.json", "r+") as f:
            data = json.load(f)
            data.append({"name": name, "path": dest_path})
            f.seek(0)
            json.dump(data, f, indent=4)

        QMessageBox.information(self, "Succès", f"Utilisateur {name} ajouté.")

    def start_detection(self):
        add_to_startup(os.path.abspath("main.py"))
        QMessageBox.information(self, "Info", "Ajouté au démarrage. Démarrage de la détection...")
        face_detection_loop()

