import cv2
import os
import numpy as np
import imutils
from PyQt6 import QtCore, QtGui

def capture_and_save(personName, cameraLabel, model, progressBar):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.dirname(current_dir)
    dataPath = os.path.join(project_dir, 'Data')
    personPath = os.path.join(dataPath, personName)

    if not os.path.exists(personPath):
        os.makedirs(personPath)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0
    total_images = 300

    while count < total_images:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=320)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (96, 96))
            rostro_blob = cv2.dnn.blobFromImage(rostro, 1.0/255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
            model.setInput(rostro_blob)
            vec = model.forward()
            np.save(os.path.join(personPath, 'rostro_{}.npy'.format(count)), vec)
            count += 1

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qt_image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format.Format_RGB888)
        cameraLabel.setPixmap(QtGui.QPixmap.fromImage(qt_image))
        QtCore.QCoreApplication.processEvents()

        progressBar.setValue(int((count / total_images) * 100))

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    progressBar.setValue(0)
