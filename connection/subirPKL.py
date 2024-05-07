import pickle
import mysql.connector
from mysql.connector import Error

# Carga los datos del archivo
with open('Models/ModeloFaceFrontalData2024.pkl', 'rb') as f:
    data = pickle.load(f)

# Serializa los datos
pickled_data = pickle.dumps(data)

try:
    cnx = mysql.connector.connect(user='root', password='',
                                host='localhost',
                                database='genlist-test')
    cursor = cnx.cursor()

    query = ("INSERT INTO `materias`(`modelo`) VALUES (%s)")
    cursor.execute(query, (pickled_data,))
    cnx.commit()
    cursor.close()
    cnx.close()
except Error as e:
    print("Ocurrio un error: ",e)
