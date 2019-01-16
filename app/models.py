from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
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
    start_hour = db.Column(db.Time, nullable=True)
    stop_time = db.Column(db.Time, nullable=True) 
    stops = db.Column(db.Integer, nullable=True)
    velocity = db.Column(db.Float, nullable=True)
    hits = db.Column(db.Integer, nullable=False, default=0)
