import os
from flask import Flask, request, render_template, send_from_directory

__author__ = 'Daniel Baulé'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/base")
def index():
    return render_template("base.html")


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/newsketch")
def newsketch():
    return render_template("newsketch.html")

if __name__ == "__main__":
    app.run(port=4555, debug=True)