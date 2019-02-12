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

# Creates a Flask application
app = Flask(__name__)

# Creates a bcrypt oobject from the flask application
bcrypt = Bcrypt(app)

if __name__ == "__main__":
    #Creates the connection to the data base
    conn, cur = connectSQL("postgres", "4RM453LDB", "localhost", "production_data")

    if conn:
        # Receive input data from the user in the console
        name = input("Ingresa un nombre: ")
        while not name.replace(" ", "").isalpha():
            print("Ingrese un nombre valido")
            name = input("Ingresa un nombre: ")
        while True:
            email = input("Ingresa un correo: ")
            if email.replace("@","").replace(".","").isalnum() and "@" in email:
                break
            else:
                print("Ingrese un correo valido")
        password = input("Ingrese el password: ")
        while not password.isalnum():
            print("Ingrese un password valido ese")
            password = input("Ingrese el password: ")

        # Encrypt the password using bcrypt object before saving it in the database
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Query and values to execute
        query = """INSERT INTO users 
                    (name, email, password)
                    VALUES (%s, %s, %s)"""
        values = (name, email, pw_hash)
        cur.execute(query, values)

        # Save changes in the data base
        conn.commit()

        # Closes the connection to the data base
        cur.close()
        conn.close()
