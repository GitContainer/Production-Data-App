import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import mysql.connector

engine = create_engine('mysql+mysqlconnector://root:Autom2018@127.0.0.1/produccion')
db = scoped_session(sessionmaker(bind=engine))

def main():
    machines = db.execute("SELECT * FROM produccion.maquina").fetchall()
    for machine in machines:
        print(machine.nombre)

if __name__ == "__main__":
    main()