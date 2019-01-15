from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True
app.env = "development"

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

if __name__ == "__main__":
    app.run(host='127.0.0.2', port=5000, debug=True)