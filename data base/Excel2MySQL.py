import mysql.connector
from datetime import date, datetime
from mysql.connector import errorcode
from time import sleep
import csv

config = {
  'user': 'root',
  'password': 'Autom2018',
  'host': '127.0.0.1',
  'database': 'produccion',
  'raise_on_warnings': True
}

def uploadData(cursor, param1, param2, param3, param4, param5, param6, param7):
    row_Info = {
      'clave_producto': param1,
      'clase': param2,
      'descripcion': param3,
      'unidad': param4,
      'peso': param5,
      'estribos': param6,
      'tramos': param7
    }
    if type(param6) == type(3):
        add_Row = ("INSERT INTO catalogo"
                    "(clave_producto, clase, descripcion, unidad, peso, estribos, tramos) "
                    "VALUES (%(clave_producto)s, %(clase)s, %(descripcion)s, %(unidad)s, %(peso)s, %(estribos)s, %(tramos)s)")
    else:
        add_Row = ("INSERT INTO catalogo"
                    "(clave_producto, clase, descripcion, unidad, peso) "
                    "VALUES (%(clave_producto)s, %(clase)s, %(descripcion)s, %(unidad)s, %(peso)s)")
    cursor.execute(add_Row, row_Info)
    
try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = cnx.cursor()
    with open('Catalogo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            clave_producto = row["clave_producto"]
            clase = row["clase"]
            descripcion = row["descripcion"]
            unidad = row["unidad"]
            peso = row["peso"]
            estribos = row["estribos"]
            tramos = row["tramos"]
            if estribos.isdigit():
                estribos = int(estribos)
            print estribos
            print type(estribos)
            uploadData(cursor, clave_producto, clase, descripcion, unidad, peso, estribos, tramos)
            cnx.commit()
    cursor.close()
    cnx.close()
