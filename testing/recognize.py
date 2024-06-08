import cv2
import numpy as np
import pickle

def recognize_face(frame, clf, model):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
    results = []

    for (x, y, w, h) in faces:
        rostro = frame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (96, 96))
        rostro_blob = cv2.dnn.blobFromImage(rostro, 1.0/255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
        model.setInput(rostro_blob)
        vec = model.forward()
        result = clf.predict([vec.flatten()])
        proba = clf.predict_proba([vec.flatten()])

        if np.max(proba) < 0.5:
            results.append((x, y, w, h, 'Desconocido'))
        else:
            results.append((x, y, w, h, result[0]))

    return results
