from flask import Flask, render_template, request, flash, redirect, url_for, Response, jsonify
from models import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from sqlalchemy import and_
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit, send
import json
from werkzeug.contrib.cache import SimpleCache
import re

app = Flask(__name__)
app.debug = True
app.env = "development"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:Autom2018@localhost/production_data'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 150
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 150
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 300
db = SQLAlchemy(app)
db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Favor de iniciar sesión"
bcrypt = Bcrypt(app)
socketio = SocketIO(app)
CACHE_TIMEOUT = 1500
cache = SimpleCache()


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        email1 = request.form['email1']
        password1 = request.form['password1']
        user = User.query.filter_by(email=email1).first()
        if user and bcrypt.check_password_hash(user.password, password1):
            login_user(user, False)
            return redirect(url_for('home'))
        else:
            flash("Credenciales incorrectas", "danger")
    return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/home", methods=['GET'])
@login_required
def home():
    return render_template('home.html')


@app.route("/record", methods=['GET'])
@login_required
def record():
    return render_template('record.html')


@app.route("/MG320", methods=['GET'])
@login_required
def MG320():
    return render_template('MG320.html')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class cached(object):

    def __init__(self, timeout=None):
        self.timeout = timeout or CACHE_TIMEOUT

    def __call__(self, f):
        def decorator(*args, **kwargs):
            response = cache.get(request.path)
            if response is None:
                response = f(*args, **kwargs)
                cache.set(request.path, response, self.timeout)
            return response
        return decorator


@socketio.on('getData')
@cached()
def refreshData():
    mg320 = Machine.query.filter_by(id='MG320').first()
    pg12 = Machine.query.filter_by(id='5S07').first()
    jager = Machine.query.filter_by(id='JAGER').first()
    schl1 = Machine.query.filter_by(id='SCHL1').first()
    schl4 = Machine.query.filter_by(id='SCHL4').first()
    schl5 = Machine.query.filter_by(id='SCHL5').first()
    schl7 = Machine.query.filter_by(id='SCHL7').first()
    new_data = {"MG320":
                {
                    "start_time": str(mg320.start_hour),
                    "stop_time": str(mg320.stop_time),
                    "stops": mg320.stops,
                    "velocity": mg320.velocity,
                    "hits": mg320.hits,
                    "hour0": mg320.hour0,
                    "hour1": mg320.hour1,
                    "hour2": mg320.hour2,
                    "hour3": mg320.hour3,
                    "hour4": mg320.hour4,
                    "hour5": mg320.hour5,
                    "hour6": mg320.hour6,
                    "hour7": mg320.hour7,
                    "hour8": mg320.hour8,
                    "hour9": mg320.hour9
                },
                "PG12":
                    {
                        "start_time": str(pg12.start_hour),
                        "stop_time": str(pg12.stop_time),
                        "stops": pg12.stops,
                        "velocity": pg12.velocity,
                        "hits": pg12.hits,
                        "hour0": pg12.hour0,
                        "hour1": pg12.hour1,
                        "hour2": pg12.hour2,
                        "hour3": pg12.hour3,
                        "hour4": pg12.hour4,
                        "hour5": pg12.hour5,
                        "hour6": pg12.hour6,
                        "hour7": pg12.hour7,
                        "hour8": pg12.hour8,
                        "hour9": pg12.hour9
                },
                "Jager":
                    {
                        "start_time": str(jager.start_hour),
                        "stop_time": str(jager.stop_time),
                        "stops": jager.stops,
                        "velocity": jager.velocity,
                        "hits": jager.hits,
                        "hour0": jager.hour0,
                        "hour1": jager.hour1,
                        "hour2": jager.hour2,
                        "hour3": jager.hour3,
                        "hour4": jager.hour4,
                        "hour5": jager.hour5,
                        "hour6": jager.hour6,
                        "hour7": jager.hour7,
                        "hour8": jager.hour8,
                        "hour9": jager.hour9
                },
                "Schlatter1":
                    {
                        "start_time": str(schl1.start_hour),
                        "stop_time": str(schl1.stop_time),
                        "stops": schl1.stops,
                        "velocity": schl1.velocity,
                        "hits": schl1.hits,
                        "hour0": schl1.hour0,
                        "hour1": schl1.hour1,
                        "hour2": schl1.hour2,
                        "hour3": schl1.hour3,
                        "hour4": schl1.hour4,
                        "hour5": schl1.hour5,
                        "hour6": schl1.hour6,
                        "hour7": schl1.hour7,
                        "hour8": schl1.hour8,
                        "hour9": schl1.hour9
                },
                "Schlatter4":
                    {
                        "start_time": str(schl4.start_hour),
                        "stop_time": str(schl4.stop_time),
                        "stops": schl4.stops,
                        "velocity": schl4.velocity,
                        "hits": schl4.hits,
                        "hour0":schl4.hour0,
                        "hour1":schl4.hour1,
                        "hour2":schl4.hour2,
                        "hour3":schl4.hour3,
                        "hour4":schl4.hour4,
                        "hour5":schl4.hour5,
                        "hour6":schl4.hour6,
                        "hour7":schl4.hour7,
                        "hour8":schl4.hour8,
                        "hour9":schl4.hour9
                },
                "Schlatter5":
                    {
                        "start_time": str(schl5.start_hour),
                        "stop_time": str(schl5.stop_time),
                        "stops": schl5.stops,
                        "velocity": schl5.velocity,
                        "hits": schl5.hits,
                        "hour0": schl5.hour0,
                        "hour1": schl5.hour1,
                        "hour2": schl5.hour2,
                        "hour3": schl5.hour3,
                        "hour4": schl5.hour4,
                        "hour5": schl5.hour5,
                        "hour6": schl5.hour6,
                        "hour7": schl5.hour7,
                        "hour8": schl5.hour8,
                        "hour9": schl5.hour9
                },
                "Schlatter7":
                    {
                        "start_time": str(schl7.start_hour),
                        "stop_time": str(schl7.stop_time),
                        "stops": schl7.stops,
                        "velocity": schl7.velocity,
                        "hits": schl7.hits,
                        "hour0": schl7.hour0,
                        "hour1": schl7.hour1,
                        "hour2": schl7.hour2,
                        "hour3": schl7.hour3,
                        "hour4": schl7.hour4,
                        "hour5": schl7.hour5,
                        "hour6": schl7.hour6,
                        "hour7": schl7.hour7,
                        "hour8": schl7.hour8,
                        "hour9": schl7.hour9
                }
    }
    db.session.remove()
    new_data = json.dumps(new_data)
    emit('new_data', new_data, broadcast=False)


@socketio.on('get annual production')
@cached()
def get_anual_production():
    production = Production.query.all()
    D = {}
    for row in production:
        d = {}
        d["date"] = row.date
        d["shift"] = row.shift
        d["machine"] = row.machine
        d["start_hour"] = str(row.start_hour)
        d["stop_time"] = str(row.stop_time)
        d["stops"] = row.stops
        d["hits"] = row.hits
        D[row.id] = d
        del d
    new_data = json.dumps(D)
    emit('annual production', new_data, broadcast=False)

if __name__ == "__main__":
    socketio.run(app)
