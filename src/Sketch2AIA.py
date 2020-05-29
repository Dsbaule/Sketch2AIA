import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for

import string, random

__author__ = 'Daniel Baulé'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def genCode(size=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


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


@app.route("/download/")
@app.route("/download/<code>")
def download(code=None):
    return render_template("download.html", code=code)

@app.route("/upload", methods=["POST"])
def upload():
    fileDirectory = os.path.join(APP_ROOT, 'files/')
    code = ""

    while True:
        code = genCode()
        targetDirectory = os.path.join(fileDirectory, code + '/')
        if not os.path.isdir(targetDirectory):
            os.mkdir(targetDirectory)
            break

    sketchList  =  list()
    for sketch in request.files.getlist("sketches"):
        filename = sketch.filename
        sketchList.append(filename)
        destination = "/".join([targetDirectory, filename])
        sketch.save(destination)

    return render_template("previewSketches.html", code=code, sketchList=sketchList)

@app.route('/view/<code>/<filename>')
def viewImage(filename='', code=''):
    print("files/" + code)
    print(filename)
    return send_from_directory("files/" + code, filename)


if __name__ == "__main__":
    app.run(port=4555, debug=True)