import os
import numpy as np
from sklearn import svm
import pickle

def train_model():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.dirname(current_dir)
    dataPath = os.path.join(project_dir, 'Data')

    peopleList = os.listdir(dataPath)
    labels = []
    facesData = []
    label = 0

    for nameDir in peopleList:
        personPath = os.path.join(dataPath, nameDir)
        for fileName in os.listdir(personPath):
            labels.append(label)
            vec = np.load(os.path.join(personPath, fileName))
            facesData.append(vec.flatten())
        label += 1

    clf = svm.SVC(gamma='scale', probability=True)
    clf.fit(facesData, np.array(labels))

    modelPath = os.path.join(project_dir, 'Models', 'ModeloFaceFrontalData2024.pkl')
    with open(modelPath, 'wb') as f:
        pickle.dump(clf, f)
