from flask import Flask, render_template, request, flash, redirect, url_for, Response
from models import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from sqlalchemy import and_
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.debug = True
app.env = "development"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:Autom2018@localhost/production_data'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

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

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def main():
    db.create_all()
    print("finished")

if __name__ == "__main__":
    with app.app_context():
        main()
    app.run(host='127.0.0.2', port=5000, debug=True)