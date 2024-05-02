import cv2
import os
import numpy as np

dataPath = r'G:\PROYECTO CONFIDENCIAL\Red Neuronal OpenCV\Data'
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

        #########################################################
        image = vec.reshape((16, 8))
        cv2.imshow('image', image)
        cv2.waitKey(10)
        #########################################################
    label = label + 1

cv2.destroyAllWindows()

# Entrenar un clasificador SVM con los embeddings de FaceNet
from sklearn import svm
clf = svm.SVC(gamma='scale', probability=True)
print("Entrenando...")
clf.fit(facesData, np.array(labels))

# Guardar el modelo entrenado
import pickle
with open('ModeloFaceFrontalData2024.pkl', 'wb') as f:
    pickle.dump(clf, f)
print('Modelo Guardado')
