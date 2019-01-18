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

class Production(db.Model):
    __tablename__ = "production"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    shift = db.Column(db.SmallInteger, nullable=False)
    machine = db.Column(db.String, nullable=False)
    start_hour = db.Column(db.Time, nullable=True)
    stop_time = db.Column(db.Time, nullable=True) 
    stops = db.Column(db.Integer, nullable=True)
    hits = db.Column(db.Integer, nullable=False, default=0)