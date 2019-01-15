from flask import Flask, render_template


app = Flask(__name__)
app.debug = True
app.env = "development"

@app.route("/")
def form():
    return render_template("form.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)