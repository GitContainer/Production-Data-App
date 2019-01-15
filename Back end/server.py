from flask import Flask

app = Flask(__name__)
app.debug = True
app.env = "development"

@app.route("/")
def index():
    return "Hello, world!!!"

@app.route("/<string:name>")
def hello(name):
    name = name.capitalize()
    return "Hello " + name + "!"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)