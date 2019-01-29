from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

app = Flask(__name__)

# Configuration
app.debug = True
app.env = "development"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:Autom2018@localhost/production_data'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 150
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 150
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 300

db = SQLAlchemy(app, session_options={'autocommit': True})
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Favor de iniciar sesión"
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

from production_data_app import routes

