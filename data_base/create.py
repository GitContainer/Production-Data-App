import csv
import sys

sys.path.append('/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/')

from production_data_app import db, app
from production_data_app.models import *

def productsUpload():
    path = '/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/data_base/products.csv'
    f = open(path)
    reader = csv.reader(f)
    next(reader)
    for key, kind, description, units, weight, cross_wires in reader:
        product = Product(id=key, kind=kind, description=description, units=units, weight=weight, cross_wires=cross_wires)
        db.session.add(product)

def machinesUpload():
    path = '/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/data_base/machines.csv'
    f = open(path)
    reader = csv.reader(f)
    next(reader)
    for id, name in reader:
        machine = Machine(id=id, name=name)
        db.session.add(machine)

if __name__ == "__main__":
    db.create_all()
    machinesUpload()
    productsUpload()
    #For this to work you need to change autocommit = FALSE 
    db.session.commit()
