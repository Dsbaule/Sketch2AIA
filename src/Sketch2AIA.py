import glob, os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, send_file

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
def downloadPage(code=None):
    if code is None:
        return render_template("getCode.html")
    else:
        fileDirectory = os.path.join(APP_ROOT, 'files/')
        targetDirectory = os.path.join(fileDirectory, code + '/')

        print(os.path.join(targetDirectory, '*.jpg'))

        imageList=list()
        for image in glob.glob(os.path.join(targetDirectory, '*.jpg')):
            imageList.append(os.path.basename(image))

        return render_template("download.html", code=code, imageList=imageList)

@app.route("/download/<code>/aia")
def getAIA(code=None):
    if code is None:
        return render_template("error.html")

    fileDirectory = os.path.join(APP_ROOT, 'files/')
    targetDirectory = os.path.join(fileDirectory, code + '/')
    try:
        return send_file(targetDirectory + "meu_projeto.aia", attachment_filename='meu_projeto.aia')
    except Exception as e:
        return render_template("error.html")

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