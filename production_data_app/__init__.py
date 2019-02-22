from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

# Create a flask application
app = Flask(__name__)

# Configuration of the flask application
app.debug = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:Autom2018@localhost/production_data'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 150
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 150
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 300

# Create an ORM connection to the database
db = SQLAlchemy(app, session_options={'autocommit': True})

# Creation and configuration of login session
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Favor de iniciar sesión"

# Create a bcrypt object for encrypting passwords
bcrypt = Bcrypt(app)

# Wrapps the flask application using a web socket from socketio
socketio = SocketIO(app)

from production_data_app import routes

