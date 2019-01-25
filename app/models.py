from flask_sqlalchemy import SQLAlchemy
from server import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.String, primary_key=True)
    kind = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    units = db.Column(db.String, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    cross_wires = db.Column(db.String, nullable=True)

class Machine(db.Model):
    __tablename__ = "machines"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_hour = db.Column(db.Time, nullable=True)
    stop_time = db.Column(db.Time, nullable=True) 
    stops = db.Column(db.Integer, nullable=True)
    velocity = db.Column(db.Integer, nullable=True)
    hits = db.Column(db.Integer, nullable=True, default=0)
    hour0 = db.Column(db.Integer, nullable=False, default=0)
    hour1 = db.Column(db.Integer, nullable=False, default=0)
    hour2 = db.Column(db.Integer, nullable=False, default=0)
    hour3 = db.Column(db.Integer, nullable=False, default=0)
    hour4 = db.Column(db.Integer, nullable=False, default=0)
    hour5 = db.Column(db.Integer, nullable=False, default=0)
    hour6 = db.Column(db.Integer, nullable=False, default=0)
    hour7 = db.Column(db.Integer, nullable=False, default=0)
    hour8 = db.Column(db.Integer, nullable=False, default=0)
    hour9 = db.Column(db.Integer, nullable=False, default=0)

class Production(db.Model):
    __tablename__ = "production"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    shift = db.Column(db.SmallInteger, nullable=False)
    machine = db.Column(db.String, nullable=False)
    start_hour = db.Column(db.Time, nullable=True)
    stop_time = db.Column(db.Time, nullable=True) 
    stops = db.Column(db.Integer, nullable=True)
    hits = db.Column(db.Integer, nullable=False, default=0)

class Velocity(db.Model):
    __tablename__ = "velocities"
    timestamp = db.Column(db.Time, primary_key=True)
    mg320 = db.Column(db.Integer, nullable = False, default=0)
    pg12 = db.Column(db.Integer, nullable = False, default=0)
    evg = db.Column(db.Integer, nullable = False, default=0)
    jager = db.Column(db.Integer, nullable = False, default=0)
    schl1 = db.Column(db.Integer, nullable = False, default=0)
    schl4 = db.Column(db.Integer, nullable = False, default=0)
    schl5 = db.Column(db.Integer, nullable = False, default=0)
    schl6 = db.Column(db.Integer, nullable = False, default=0)
    schl7 = db.Column(db.Integer, nullable = False, default=0)