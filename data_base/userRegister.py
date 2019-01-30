from flask import Flask
from flask_bcrypt import Bcrypt
import psycopg2

def connectSQL(user, password, host, database):
    conn = None
    try:
        conn = psycopg2.connect(
            host=host, database=database, user=user, password=password)
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        return (None, error)
    else:
        return (conn, cur)



app = Flask(__name__)
bcrypt = Bcrypt(app)

if __name__ == "__main__":
    conn, cur = connectSQL("postgres", "Autom2018", "localhost", "production_data")
    if conn:
        name = input("Ingresa un nombre: ")
        while not name.replace(" ", "").isalpha():
            print("Ingrese un nombre válido")
            name = input("Ingresa un nombre: ")
        while True:
            email = input("Ingresa un correo: ")
            if email.replace("@","").replace(".","").isalnum() and "@" in email:
                break
            else:
                print("Ingrese un correo válido")
        password = input("Ingrese la contraseña: ")
        while not password.isalnum():
            print("Ingrese una contraseña válida")
            password = input("Ingrese la contraseña: ")
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        query = """INSERT INTO users 
                    (name, email, password)
                    VALUES (%s, %s, %s)"""
        values = (name, email, pw_hash)
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()