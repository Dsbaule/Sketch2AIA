import glob, os
import time

from flask import Flask, request, render_template, send_from_directory, redirect, url_for, send_file, session

import string, random
import shutil

__author__ = 'Daniel Baulé'

app = Flask(__name__)
app.secret_key = 'Sketch2AIAsessionsecretkey'

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

    session['code'] = code

    sketchList  =  list()
    for sketch in request.files.getlist("sketches"):
        filename = sketch.filename
        sketchList.append(filename)
        destination = "/".join([targetDirectory, filename])
        sketch.save(destination)

    return render_template("previewSketches.html", code=code, sketchList=sketchList)


@app.route("/upload/confirm", methods=["POST"])
def genAIA():
    print(request.form)
    time.sleep(5)
    return redirect(url_for("downloadPage", code=session.pop('code', None)))

@app.route("/upload/cancel")
def cancelUpload():
    code = session.pop('code', None)

    if code is not None:
        fileDirectory = os.path.join(APP_ROOT, 'files/')
        targetDirectory = os.path.join(fileDirectory, code + '/')

        try:
            shutil.rmtree(targetDirectory)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))

    return redirect(url_for('home'))


@app.route("/download/")
@app.route("/download/<show_error>")
def getCode(show_error=False):
    return render_template("getCode.html", show_error=show_error)


@app.route("/findcode/", methods=["POST"])
def findCode():
    return redirect(url_for("downloadPage", code=request.form['code']))


@app.route("/download/files/<code>")
def downloadPage(code=None):
    if code is None:
        return redirect(url_for('getCode', show_error=0))
    else:
        fileDirectory = os.path.join(APP_ROOT, 'files/')
        targetDirectory = os.path.join(fileDirectory, code + '/')

        if not os.path.isdir(targetDirectory):
            return redirect(url_for('getCode', show_error=0))

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
    aiaFile = os.path.join(targetDirectory, 'meu_projeto.aia')

    try:
        return send_file(aiaFile, as_attachment=True, mimetype='application/octet-stream', attachment_filename='teste.aia')
    except Exception as e:
        return render_template("error.html")


@app.route('/view/<code>/<filename>')
def viewImage(filename='', code=''):
    print("files/" + code)
    print(filename)
    return send_from_directory("files/" + code, filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4555, debug=True)