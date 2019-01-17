from flask import Flask, render_template, request, flash, redirect, url_for, Response
from models import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.debug = True
app.env = "development"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:Autom2018@localhost/production_data'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager(app)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
      if request.form['email1'] != 'julio.sanchez@armasel.com' or \
         request.form['password1'] != 'Autom2018':
         error = 'Invalid username or password. Please try again!'
      else:
          user = User()
          login_user(user)
          return render_template('table.html')
    return render_template('form.html', error = error)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
    app.run(host='127.0.0.2', port=5000, debug=True)