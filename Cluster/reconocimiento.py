import cv2
import os
import numpy as np
import pickle

dataPath = r'G:\PROYECTO CONFIDENCIAL\Red Neuronal OpenCV\Data2'
imagePaths = os.listdir(dataPath)
print('imagePaths', imagePaths)

# Cargar el modelo pre-entrenado de FaceNet
model = cv2.dnn.readNetFromTorch('openface.nn4.small2.v1.t7')

# Cargar el clasificador SVM entrenado
with open('Models/ModeloFaceFrontalData2024.pkl', 'rb') as f:
    clf = pickle.load(f)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if ret == False: break
    auxFrame = frame.copy()

    faces = faceClassif.detectMultiScale(frame, 1.3, 5)
    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (96, 96))
        rostro_blob = cv2.dnn.blobFromImage(rostro, 1.0/255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
        model.setInput(rostro_blob)
        vec = model.forward()
        result = clf.predict([vec.flatten()])

        cv2.putText(frame, '{}'.format(result),(x, y-5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

        if result[0] < 70:
            cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y-25), 2, 1.1,(0, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Desconocido', (x,y-20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)
    
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
