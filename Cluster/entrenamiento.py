import cv2
import os
import numpy as np
from sklearn import svm
import pickle

# Obtiene la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Sube un nivel en la estructura de directorios
project_dir = os.path.dirname(current_dir)

# Une la ruta del directorio del proyecto con la carpeta 'Data'
dataPath = os.path.join(project_dir, 'Data')
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
