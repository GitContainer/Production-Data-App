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
app.config["SQLALCHEMY_POOL_SIZE"] = 3600
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 500
db = SQLAlchemy(app)
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
    return render_template('login.html', error = error)

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

@socketio.on('refresh table data')
@cached()
def refresh_table_data():
    new_data = {"MG320": 
                    {
                        "start_time": str(Machine.query.filter_by(id='MG320').first().start_hour),
                        "stop_time": str(Machine.query.filter_by(id='MG320').first().stop_time),
                        "stops": Machine.query.filter_by(id='MG320').first().stops,
                        "velocity": Machine.query.filter_by(id='MG320').first().velocity,
                        "hits": Machine.query.filter_by(id='MG320').first().hits     
                    },
                "PG12":
                    {
                        "start_time": str(Machine.query.filter_by(id='5S07').first().start_hour),
                        "stop_time": str(Machine.query.filter_by(id='5S07').first().stop_time),
                        "stops": Machine.query.filter_by(id='5S07').first().stops,
                        "velocity": Machine.query.filter_by(id='5S07').first().velocity,
                        "hits": Machine.query.filter_by(id='5S07').first().hits                    
                    },
                "Jager":
                    {
                        "start_time": str(Machine.query.filter_by(id='JAGER').first().start_hour),
                        "stop_time": str(Machine.query.filter_by(id='JAGER').first().stop_time),
                        "stops": Machine.query.filter_by(id='JAGER').first().stops,
                        "velocity": Machine.query.filter_by(id='JAGER').first().velocity,
                        "hits": Machine.query.filter_by(id='JAGER').first().hits                         
                    },
                "Schlatter1":
                    {
                        "start_time": str(Machine.query.filter_by(id='SCHL1').first().start_hour),
                        "stop_time": str(Machine.query.filter_by(id='SCHL1').first().stop_time),
                        "stops": Machine.query.filter_by(id='SCHL1').first().stops,
                        "velocity": Machine.query.filter_by(id='SCHL1').first().velocity,
                        "hits": Machine.query.filter_by(id='SCHL1').first().hits                      
                    },
                "Schlatter4":
                    {
                        "start_time": str(Machine.query.filter_by(id='SCHL4').first().start_hour),
                        "stop_time": str(Machine.query.filter_by(id='SCHL4').first().stop_time),
                        "stops": Machine.query.filter_by(id='SCHL4').first().stops,
                        "velocity": Machine.query.filter_by(id='SCHL4').first().velocity,
                        "hits": Machine.query.filter_by(id='SCHL4').first().hits                        
                    },
                "Schlatter5":
                    {
                        "start_time": str(Machine.query.filter_by(id='SCHL5').first().start_hour),
                        "stop_time": str(Machine.query.filter_by(id='SCHL5').first().stop_time),
                        "stops": Machine.query.filter_by(id='SCHL5').first().stops,
                        "velocity": Machine.query.filter_by(id='SCHL5').first().velocity,
                        "hits": Machine.query.filter_by(id='SCHL5').first().hits                        
                    },
                "Schlatter7":
                    {
                        "start_time": str(Machine.query.filter_by(id='SCHL7').first().start_hour),
                        "stop_time": str(Machine.query.filter_by(id='SCHL7').first().stop_time),
                        "stops": Machine.query.filter_by(id='SCHL7').first().stops,
                        "velocity": Machine.query.filter_by(id='SCHL7').first().velocity,
                        "hits": Machine.query.filter_by(id='SCHL7').first().hits                      
                    }                                                                                
                }
    new_data = json.dumps(new_data)
    emit('table data', new_data, broadcast=False)

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

@socketio.on('request MG320 data')
@cached()
def get_MG320_data():
    hits = Machine.query.filter_by(id='MG320').first().hits
    emit('MG320 data', hits, broadcast=False)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
        socketio.run(app)
        #app.run(host='127.0.0.2', port=5000, debug=True)