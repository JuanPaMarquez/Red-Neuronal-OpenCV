import mysql.connector
import pickle
from mysql.connector import Error

try:
    cnx = mysql.connector.connect(user='root', password='',
                                host='localhost',
                                database='genlist-test')
    cursor = cnx.cursor()

    query = ("SELECT modelo FROM materias WHERE id = 1")
    cursor.execute(query)

    for (pickled_data,) in cursor:
        # Deserializa los datos
        data = pickle.loads(pickled_data)
        # Guarda los datos en un archivo .pkl
        with open('ModeloFaceFrontalData2024.pkl', 'wb') as f:
            pickle.dump(data, f)

    cursor.close()
    cnx.close()
except Error as e:
    print("Ocurrio un error: ",e)
