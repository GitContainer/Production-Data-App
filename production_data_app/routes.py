from flask import render_template, request, flash, redirect, url_for, Response, jsonify
from flask_login import login_required, login_user, logout_user, current_user
import json
from production_data_app import app, bcrypt, login_manager, socketio
from werkzeug.contrib.cache import SimpleCache
from flask_socketio import emit
from sqlalchemy import desc
from production_data_app.models import User, Production, Velocity, Machine
import collections

# Amount of time flask is going to keep database queries results whenever it receives a consult
CACHE_TIMEOUT = 1500

# Create cahe object
cache = SimpleCache()

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

@app.route("/")
def index():
    """Default page, if the user has alredy logged in he will be redirected to the home page, 
    otherwise he is going to be redirected to the login page."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login function that is only called by the login page whenever a user tries to login,
    this function gets the submit information and verifies that the data matches with the db data.
    If the information is validated, then the function redirects the user to the home page and creates
    a login object for the user."""
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
    """This function logs out the user using the login object, so the user will be automatically redirected to the login page"""
    logout_user()
    return redirect(url_for('login'))


@app.route("/home", methods=['GET'])
@login_required
def home():
    """Redirects to the home page which has the main table (the one that has general information of all the machines"""
    return render_template('home.html')


@app.route("/record")
@login_required
def record():
    """Redirects to the record page which has the history record of the production data in a table"""
    production = Production.query.order_by(desc(Production.id)).all()
    return render_template('record.html', production=production)

@app.route("/prodperhour", methods=['GET'])
@login_required
def prodperhour():
    """Redirects to the production per hour page which has bar charts of every machine's hourly production"""
    return render_template('prodperhour.html')


@app.route("/MG320", methods=['GET'])
@login_required
def MG320():
    """Returns MG320 page which has detailed information about the real time production data of this machine"""
    return render_template('MG320.html')


@app.route("/PG12", methods=['GET'])
@login_required
def PG12():
    """Returns PG12 page which has detailed information about the real time production data of this machine"""
    return render_template('PG12.html')


@app.route("/Jager", methods=['GET'])
@login_required
def Jager():
    """Returns Jager page which has detailed information about the real time production data of this machine"""
    return render_template('Jager.html')


@app.route("/Schlatter_1", methods=['GET'])
@login_required
def Schlatter_1():
    """Returns Schlatter 1 page which has detailed information about the real time production data of this machine"""
    return render_template('Schlatter_1.html')


@app.route("/Schlatter_4", methods=['GET'])
@login_required
def Schlatter_4():
    """Returns Schlatter 4 page which has detailed information about the real time production data of this machine"""
    return render_template('Schlatter_4.html')


@app.route("/Schlatter_5", methods=['GET'])
@login_required
def Schlatter_5():
    """Returns Schlatter 5 page which has detailed information about the real time production data of this machine"""
    return render_template('Schlatter_5.html')


@app.route("/Schlatter_7", methods=['GET'])
@login_required
def Schlatter_7():
    """Returns Schlatter 7 page which has detailed information about the real time production data of this machine"""
    return render_template('Schlatter_7.html')


@login_manager.user_loader
def load_user(id):
    """Function that returns the id number of a particular user"""
    return User.query.get(int(id))


@socketio.on('getData')
@cached()
def refreshData():
    """Function that gets called on a socket io request that downloads all the general information
    about the machines from the data base, wrapps it into a dictionary and then it returns, whith 
    a socket io emit, the dictionary parsed into a JSON format object"""

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
                    "last_stop": str(mg320.last_stop),
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
                        "last_stop": str(pg12.last_stop),
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
                        "last_stop": str(jager.last_stop),
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
                        "last_stop": str(schl1.last_stop),
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
                        "last_stop": str(schl4.last_stop),
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
                        "last_stop": str(schl5.last_stop),
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
                        "last_stop": str(schl7.last_stop),
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
    new_data = json.dumps(new_data)
    emit('new_data', new_data, broadcast=False)

@socketio.on('getVelocities')
@cached()
def getVelocities():
    """Function that gets called on a socket io request that downloads all the velocities values
    about the machines from the data base, wrapps it into an ordered dictionary and then it returns, whith 
    a socket io emit, the ordered dictionary parsed into a JSON format object"""
    velocities = Velocity.query.all()
    D = collections.OrderedDict()
    i = 0
    for row in velocities:
        d = {}
        d["timestamp"] = str(row.timestamp)
        d["mg320"] = row.mg320
        d["pg12"] = row.pg12
        d["jager"] = row.jager
        d["schl1"] = row.schl1
        d["schl4"] = row.schl4
        d["schl5"] = row.schl5
        d["schl7"] = row.schl7
        row_number = str(i)
        i += 1
        D[row_number] = d
        del d
    new_velocities = json.dumps(D, sort_keys=True)
    emit('new_velocities', new_velocities, broadcast=False)