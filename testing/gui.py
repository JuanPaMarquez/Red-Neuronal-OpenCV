from PyQt6 import QtWidgets, QtCore, QtGui
import sys
import cv2
import os
import numpy as np
import pickle
from capture_and_save import capture_and_save
from train_model import train_model
from recognize import recognize_face

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.captureButton = QtWidgets.QPushButton("Capturar y Guardar")
        self.trainButton = QtWidgets.QPushButton("Entrenar Modelo")
        self.recognizeButton = QtWidgets.QPushButton("Iniciar Reconocimiento")
        self.identifyButton = QtWidgets.QPushButton("Identificar Persona")
        self.cameraLabel = QtWidgets.QLabel()
        self.progressBar = QtWidgets.QProgressBar()
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.captureButton)
        self.layout.addWidget(self.trainButton)
        self.layout.addWidget(self.recognizeButton)
        self.layout.addWidget(self.identifyButton)
        self.layout.addWidget(self.cameraLabel)
        self.layout.addWidget(self.progressBar)
        
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)
        
        self.captureButton.clicked.connect(self.capture)
        self.trainButton.clicked.connect(self.train)
        
        self.recognizeButton.clicked.connect(self.start_recognition)
        self.identifyButton.clicked.connect(self.identify_person)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        
        self.cap = None
        self.is_capturing = False
        self.is_recognizing = False
        self.model = None
        self.clf = None
    
    def capture(self):
        personName, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Ingrese el nombre de la persona:')
        if ok:
            self.start_camera()
            self.is_capturing = True
            self.personName = personName
            self.model = cv2.dnn.readNetFromTorch('openface.nn4.small2.v1.t7')
    
    def train(self):
        train_model()
        QtWidgets.QMessageBox.information(self, "Entrenamiento", "Modelo entrenado y guardado exitosamente.")
    
    def start_recognition(self):
        self.start_camera()
        self.is_recognizing = True
        self.load_model()
    
    def identify_person(self):
        if self.is_recognizing and self.cap:
            ret, frame = self.cap.read()
            if ret:
                results = recognize_face(frame, self.clf, self.model)
                for (x, y, w, h, label) in results:
                    if label == 'Desconocido':
                        message = 'Desconocido'
                    else:
                        personName = self.get_person_name(label)
                        message = f'Persona reconocida: {personName}'
                    QtWidgets.QMessageBox.information(self, "Reconocimiento", message)
                    return
    
    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.timer.start(30)
    
    def stop_camera(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format.Format_RGB888)
            self.cameraLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            
            if self.is_capturing:
                capture_and_save(self.personName, self.cameraLabel, self.model, self.progressBar)
                self.is_capturing = False
            elif self.is_recognizing:
                self.display_recognition(frame)
        else:
            self.stop_camera()
    
    def display_recognition(self, frame):
        results = recognize_face(frame, self.clf, self.model)
        for (x, y, w, h, label) in results:
            if label == 'Desconocido':
                cv2.putText(frame, 'Desconocido', (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            else:
                personName = self.get_person_name(label)
                cv2.putText(frame, personName, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format.Format_RGB888)
        self.cameraLabel.setPixmap(QtGui.QPixmap.fromImage(image))
    
    def load_model(self):
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'Models', 'ModeloFaceFrontalData2024.pkl')
        with open(model_path, 'rb') as f:
            self.clf = pickle.load(f)
        self.model = cv2.dnn.readNetFromTorch('openface.nn4.small2.v1.t7')
    
    def get_person_name(self, label):
        dataPath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'Data')
        peopleList = os.listdir(dataPath)
        return peopleList[label]
    
    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
