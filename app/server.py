from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.debug = True
app.env = "development"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:Autom2018@localhost/production_data'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/table", methods=["POST"])
def table():
    email = request.form.get("email1")
    password = request.form.get("password1")
    if email == "julio.sanchez@armasel.com" and password == "Autom2018":
        return render_template("table.html")
    else:
        return "Datos incorrectos, regrese a la página de inicio para volver a intentarlo."

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
    #app.run(host='127.0.0.2', port=5000, debug=True)