import multiprocessing
import cv2
import os
import numpy as np
import imutils
from sklearn import svm
import pickle

# Obtiene la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Sube un nivel en la estructura de directorios
project_dir = os.path.dirname(current_dir)

# Une la ruta del directorio del proyecto con la carpeta 'Data'
dataPath = os.path.join(project_dir, 'Data')

def capture_and_save(personName):
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
        if k == 27 or count >= 300:
            break

    cap.release()
    cv2.destroyAllWindows()

def train_model():
    peopleList = os.listdir(dataPath)
    print('Lista de Personas: ', peopleList)

    labels = []
    facesData = []
    label = 0

    for nameDir in peopleList:
        personPath = dataPath + '/' + nameDir
        print('Leyendo imagenes')

        for fileName in os.listdir(personPath):
            print('Rostros: ', nameDir + '/' + fileName)
            labels.append(label)

            vec = np.load(personPath + '/' + fileName)
            facesData.append(vec.flatten())
            
        label = label + 1

    cv2.destroyAllWindows()

    # Entrenar un clasificador SVM con los embeddings de FaceNet
    clf = svm.SVC(gamma='scale', probability=True)
    print("Entrenando...")
    clf.fit(facesData, np.array(labels))

    # Guardar el modelo entrenado
    with open('Models/ModeloFaceFrontalData2024.pkl', 'wb') as f:
        pickle.dump(clf, f)
    print('Modelo Guardado')

if __name__ == '__main__':
    while True:
        personName = input("Ingrese el nombre de la persona (o 'salir' para terminar): ")
        if personName.lower() == 'salir':
            break
        p1 = multiprocessing.Process(target=capture_and_save, args=(personName,))
        p1.start()
        p1.join()

    p2 = multiprocessing.Process(target=train_model)
    p2.start()
    p2.join()

