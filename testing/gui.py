from PyQt6 import QtWidgets, QtCore
import sys
import cv2
import os
import numpy as np
import pickle
import multiprocessing
import imutils
from sklearn import svm

# Importa las funciones de tus otros archivos
from capture_and_save import capture_and_save
from train_model import train_model
from recognize import recognize

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.captureButton = QtWidgets.QPushButton("Capturar y Guardar")
        self.trainButton = QtWidgets.QPushButton("Entrenar Modelo")
        self.recognizeButton = QtWidgets.QPushButton("Reconocer")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.captureButton)
        self.layout.addWidget(self.trainButton)
        self.layout.addWidget(self.recognizeButton)

        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.captureButton.clicked.connect(self.capture)
        self.trainButton.clicked.connect(self.train)
        self.recognizeButton.clicked.connect(self.recognize)

    def capture(self):
        personName = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Ingrese el nombre de la persona:')
        if personName[1]:
            p1 = multiprocessing.Process(target=capture_and_save, args=(personName[0],))
            p1.start()
            p1.join()

    def train(self):
        p2 = multiprocessing.Process(target=train_model)
        p2.start()
        p2.join()

    def recognize(self):
        recognize()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
