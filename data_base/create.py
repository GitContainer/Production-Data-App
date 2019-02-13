import csv
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append('/home/ubntuadmin/applications/Production-Data-App/')

from production_data_app import db, app
from production_data_app.models import *

# an Engine, which the Session will use for connection resources
engine = create_engine('postgresql+psycopg2://postgres:4RM453LDB@localhost/production_data')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

def productsUpload():
    """ Takes the products data from a csv file and uploads it to the db """
    path = '/home/ubntuadmin/applications/Production-Data-App/data_base/products.csv'
    f = open(path)
    reader = csv.reader(f)
    next(reader)
    for key, kind, description, units, weight, cross_wires in reader:
        product = Product(id=key, kind=kind, description=description, units=units, weight=weight, cross_wires=cross_wires)
        session.add(product)

def machinesUpload():
    """ Takes the id and name of each machine from a csv file and uploads it to the db so the app can work """    
    path = '/home/ubntuadmin/applications/Production-Data-App/data_base/machines.csv'
    f = open(path)
    reader = csv.reader(f)
    next(reader)
    for id, name in reader:
        machine = Machine(id=id, name=name)
        session.add(machine)

if __name__ == "__main__":
    # Creates the tables of the db
    db.create_all()

    # Fill the tables with the minimum necessary data
    machinesUpload()
    productsUpload()

    # Save the changes to the db
    session.commit()
