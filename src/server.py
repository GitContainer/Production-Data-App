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
    return render_template("table.html", name=email)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)