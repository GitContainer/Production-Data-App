import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2

engine = create_engine('postgresql+psycopg2://postgres:Autom2018@localhost/lecture3')
db = scoped_session(sessionmaker(bind=engine))

def main():
    flights = db.execute("SELECT * FROM flights").fetchall()
    for flight in flights:
        print(flight.id, flight.origin, flight.destination, flight.duration)

if __name__ == "__main__":
    main()
