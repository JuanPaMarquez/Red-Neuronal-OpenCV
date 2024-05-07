from cryptography.fernet import Fernet
import pickle
import mysql.connector
from mysql.connector import Error

# Genera una clave de encriptación
key = b'TlujHsjy_nRsj5csGvZqdx7oK2C68cLDsq-VNR_oAt4='  # Reemplaza esto con tu clave
cipher_suite = Fernet(key)

# Carga los datos del archivo
with open('Models/ModeloFaceFrontalData2024.pkl', 'rb') as f:
    data = pickle.load(f)

# Serializa y encripta los datos
pickled_data = pickle.dumps(data)
encrypted_data = cipher_suite.encrypt(pickled_data)

try:
    cnx = mysql.connector.connect(user='root', password='',
                                host='localhost',
                                database='genlist-test')
    cursor = cnx.cursor()

    query = ("INSERT INTO `materias`(`modelo`) VALUES (%s)")
    cursor.execute(query, (encrypted_data,))
    cnx.commit()
    cursor.close()
    cnx.close()
except Error as e:
    print("Ocurrio un error: ",e)