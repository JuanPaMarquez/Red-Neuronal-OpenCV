import cv2
import os
import numpy as np
import imutils

personName = 'Junior Silva'
dataPath = r'G:\PROYECTO CONFIDENCIAL\Red Neuronal OpenCV\Data'
personPath = dataPath + '/' + personName

# Cargar el modelo pre-entrenado de FaceNet
model = cv2.dnn.readNetFromTorch('openface.nn4.small2.v1.t7')

if not os.path.exists(personPath):
    print('Carpeta Creada: ', personPath)
    os.makedirs(personPath)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

count = 0

while True:
    ret, frame = cap.read()
    if ret == False:
        break

    frame = imutils.resize(frame, width=320)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()

    # Detectar rostros en la imagen
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (96, 96))
        rostro_blob = cv2.dnn.blobFromImage(rostro, 1.0/255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
        model.setInput(rostro_blob)
        vec = model.forward()
        np.save(personPath + '/rostro_{}.npy'.format(count), vec)
        count = count + 1
        print(count)

    cv2.imshow('frame', frame)

    k = cv2.waitKey(1)
    if k == 27 or count >= 1000:
        break

cap.release()
cv2.destroyAllWindows()
