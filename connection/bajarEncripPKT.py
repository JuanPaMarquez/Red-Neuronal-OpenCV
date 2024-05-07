import mysql.connector
import pickle
from cryptography.fernet import Fernet
from mysql.connector import Error


# Asegúrate de usar la misma clave que usaste para encriptar los datos
key = b'TlujHsjy_nRsj5csGvZqdx7oK2C68cLDsq-VNR_oAt4='  # Reemplaza esto con tu clave
cipher_suite = Fernet(key)

try:
    cnx = mysql.connector.connect(user='root', password='',
                                host='localhost',
                                database='genlist-test')
    cursor = cnx.cursor()

    query = ("SELECT modelo FROM materias WHERE id = 3")
    cursor.execute(query)

    for (encrypted_data,) in cursor:
        # Desencripta y deserializa los datos
        pickled_data = cipher_suite.decrypt(encrypted_data)
        data = pickle.loads(pickled_data)
        # Guarda los datos en un archivo .pkl
        with open('ModeloFaceFrontalData2024.pkl', 'wb') as f:
            pickle.dump(data, f)

    cursor.close()
    cnx.close()
except Error as e:
    print("Ocurrio un error: ",e)
