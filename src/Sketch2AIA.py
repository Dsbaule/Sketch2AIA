from flask import Flask, request, render_template, send_from_directory, redirect, url_for, send_file, session
from flask.logging import create_logger
import glob, os, shutil
import time, random, string
from PIL import Image, ExifTags
import logging
import threading

from src.AIAGeneration import Detection

__author__ = 'Daniel Baulé'

app = Flask(__name__)
app.secret_key = 'Sketch2AIAsessionsecretkey'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Logging configuration:
logging_file = os.path.join(APP_ROOT, 'logs', 'app.log')
logging.basicConfig(filename=logging_file, level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s')
logger = create_logger(app)

# Mutex creation
detector_lock = threading.RLock()

# Char array for valid filenames
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

def genCode(size=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


@app.route("/")
def index():
    return redirect(url_for('howto'))


@app.route("/home")
def home():
    return redirect(url_for('howto'))
    #return render_template("home.html")


@app.route("/howto")
def howto():
    return render_template("howto.html")


@app.route("/newsketch")
def newsketch():
    return render_template("newsketch.html")


@app.route("/upload", methods=["POST"])
def upload():
    # First check if number of images <= 6
    if len(request.files.getlist("sketches")) > 6:
        logger.warning("{} - Attempted to upload more than 6 images".format(request.remote_addr))
        return render_template('error.html')


    fileDirectory = os.path.join(APP_ROOT, 'files/')
    code = ""

    # Get a new code and create folder  for images
    while True:
        code = genCode()
        targetDirectory = os.path.join(fileDirectory, code + '/')
        if not os.path.isdir(targetDirectory):
            os.mkdir(targetDirectory)
            logger.debug("{} - Created folder for code |{}|".format(request.remote_addr, code))
            break
    
    # Set flask session data
    session['code'] = code
    session['dir'] = targetDirectory

    # Create folder for original images
    originalImageDirectory = os.path.join(targetDirectory, 'original')
    os.mkdir(originalImageDirectory)
    # Create folder for detection preview    
    previewImageDirectory = os.path.join(targetDirectory, 'preview')
    os.mkdir(previewImageDirectory)
    
    # For each sketch uploaded, normalize and save it
    sketchList  =  list()
    for sketch in request.files.getlist("sketches"):
        try:
            # Pillow image check
            image = Image.open(sketch.stream)
            image.verify()
            # Reopening (image.verify makes the image object unreadable)
            image = Image.open(sketch.stream)

            # Get orientation exif tag
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            
            # If image has orientation exif tag, rotate it
            try:
                if image._getexif() is not None:
                    exif = dict(image._getexif().items())
                    
                    if orientation in exif:
                        if exif[orientation] == 3:
                            image = image.rotate(180, expand=True)
                        elif exif[orientation] == 6:
                            image = image.rotate(270, expand=True)
                        elif exif[orientation] == 8:
                            image = image.rotate(90, expand=True)
            # If image has no exif tag, do nothing
            except AttributeError:
                logger.info("{} - Image |{}| from code |{}| has no exif".format(request.remote_addr, sketch.filename, session['code']))
            except:
                return render_template('error.html')

            # Resize and convert to RGB
            image = image.resize((720,1280))
            image = image.convert('RGB')

            # Get a valid .jpg file path from image filename
            (filename, _) = os.path.splitext(sketch.filename)
            filename = ''.join(c for c in filename if c in valid_chars)
            filename = filename.replace(' ','_')
            filename += '.jpg'
            destination = os.path.join(originalImageDirectory, filename)

            # Add to list of sketches and save file
            sketchList.append(filename)
            image.save(destination)
            logger.debug("{} - Image |{}| from code |{}|saved".format(request.remote_addr, sketch.filename, session['code']))
        except:
            # If something went wrong, log and redirect to error page
            logger.warning("{} - Image |{}| from code |{}| generated an ERROR".format(request.remote_addr, sketch.filename, session['code']))
            return render_template('error.html')

    # Add list of sketches to session
    session['sketchList'] = sketchList

    # Redirect to preview page
    return render_template("previewSketches.html", code=code, sketchList=sketchList)

@app.route("/upload/confirm", methods=["POST"])
def genAIA():
    # Get data from form
    mainScreen = int(request.form['telaPrincipal'])
    listType = int(request.form['tipoLista'])
    projectName = request.form['nomeProjeto']

    # Normalize project name
    projectName = ''.join(c for c in projectName if c in valid_chars)
    projectName = projectName.replace(' ','_')
    if len(projectName) == 0:
        projectName = 'MeuProjeto'

    # Generate project (with mutex)
    logger.info("{} - Attempting to generate project |{}| with main screen |{}| and using |{}|.".format(request.remote_addr, projectName, mainScreen, request.form['tipoLista']))
    detector_lock.acquire()
    logger.debug("{} - Got detector lock".format(request.remote_addr))
    Detection.detect(projectPath=session['dir'], sketchList=session['sketchList'], mainScreen = mainScreen, projectName=projectName, listType=listType)
    detector_lock.release()
    logger.debug("{} - Got released detector lock".format(request.remote_addr))
    logger.info("{} - Project generated.".format(request.remote_addr))

    # Redirect to download page
    return redirect(url_for("downloadPage", code=session.pop('code', None)))

@app.route("/upload/cancel")
def cancelUpload():
    logger.debug("{} - Project for code |{}| canceled".format(request.remote_addr, session['code']))

    # Remove session data
    code = session.pop('code', None)
    session.pop('sketchList', None)
    session.pop('dir', None)

    # Delete files
    if code is not None:
        fileDirectory = os.path.join(APP_ROOT, 'files/')
        targetDirectory = os.path.join(fileDirectory, code + '/')
        try:
            shutil.rmtree(targetDirectory)
            logger.debug("{} - Folder for code |{}| deleted".format(request.remote_addr, code))
        except OSError as e:
            logger.warning("{} - Unable to delete folder for code |{}|".format(request.remote_addr, code))

    # Redirect to home
    return redirect(url_for('home'))


@app.route("/download/")
@app.route("/download/<show_error>")
def getCode(show_error=False):
    return render_template("getCode.html", show_error=show_error)


@app.route("/findcode/", methods=["POST"])
def findCode():
    return redirect(url_for("downloadPage", code=request.form['code'].upper()))


@app.route("/download/files/<code>")
def downloadPage(code=None):
    if code is None:
        return redirect(url_for('getCode', show_error=0))

    fileDirectory = os.path.join(APP_ROOT, 'files/')
    targetDirectory = os.path.join(fileDirectory, code + '/original/')

    if not os.path.isdir(targetDirectory):
        return redirect(url_for('getCode', show_error=0))

    imageList=list()
    for image in glob.glob(os.path.join(targetDirectory, '*.jpg')):
        imageList.append(os.path.basename(image))
    for image in glob.glob(os.path.join(targetDirectory, '*.jpeg')):
        imageList.append(os.path.basename(image))

    return render_template("download.html", code=code, imageList=imageList)


@app.route("/download/files/<code>/aia")
def getAIA(code=None):
    if code is None:
        return render_template("error.html")

    fileDirectory = os.path.join(APP_ROOT, 'files/')
    targetDirectory = os.path.join(fileDirectory, code + '/')
    aiaFile = os.path.join(targetDirectory, '*.aia')

    try:
        return send_file(glob.glob(aiaFile).pop(), as_attachment=True, mimetype='application/octet-stream')
    except Exception as e:
        logger.warning("{} - Unable to get .aia for code |{}|".format(request.remote_addr, code))
        return render_template("error.html")


@app.route('/view/image/<code>/<filename>')
def viewImage(filename='', code=''):
    return send_from_directory("files/" + code + '/original', filename)


@app.route('/view/preview/<code>/<filename>')
def viewPreview(filename='', code=''):
    return send_from_directory("files/" + code + '/preview', filename)

@app.route('/about/')
@app.route('/about/<page>')
def about(page='sketch2aia'):
    if page == 'sketch2aia':
        return render_template("about/sketch2aia.html")
    elif page == 'privacy-policy':
        return render_template("about/privacy-policy.html")
    elif page == 'terms-of-service':
        return render_template("about/terms-of-service.html")

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4555, debug=True)