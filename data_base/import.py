import csv
import sys

sys.path.append('C:\\Users\\automatizacion\\Desktop\\Git Projects\\production-data-app\\app')
# sys.path.append('D:\\Projects\\production-data-app\\app')

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from production_data_app.models import *

engine = create_engine('postgresql+psycopg2://postgres:Autom2018@localhost/production_data')
db = scoped_session(sessionmaker(bind=engine))

def productsUpload():
    # path = "C:\\Users\\automatizacion\\Desktop\\Git Projects\\Production-Data-App\\data_base\\products.csv"
    # path = "D:\\Projects\\Production-Data-App\\data_base\\products.csv"
    path = '/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/data_base/products.csv'
    f = open(path)
    reader = csv.reader(f)
    next(reader)
    for key, kind, description, units, weight, cross_wires in reader:
        product = Product(id=key, kind=kind, description=description, units=units, weight=weight, cross_wires=cross_wires)
        db.add(product)
        # print(f"Added product {key}.")
    db.commit()

def machinesUpload():
    # path = "C:\\Users\\automatizacion\\Desktop\\Git Projects\\Production-Data-App\\data_base\\products.csv"
    # path = "D:\\Projects\\production-data-app\\data base\\machines.csv"
    path = '/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/data_base/machines.csv'
    f = open(path)
    reader = csv.reader(f)
    next(reader)
    for id, name in reader:
        machine = Machine(id=id, name=name)
        db.add(machine)
        # print(f"Added machine {id} with name: {name}.")
    db.commit()

if __name__ == "__main__":
    # machinesUpload()
    usersUpload()
    # productsUpload()
