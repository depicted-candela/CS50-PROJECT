import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import login_required, add_static_image_to_audio

# Configure application
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path,'input')
RESULTS_FOLDER = os.path.join(app.root_path,'output')

# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_PATH'] = 7000000

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def intro():
    return render_template("intro.html", forward=1)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure that username was submitted
        if not username and not password and not confirmation:
            return render_template('register.html', error=1)

        # Ensure that username and password was submitted
        elif not username and not password:
            return render_template('register.html', error=2)

        # Ensure that username and password was submitted
        elif not username and not confirmation:
            return render_template('register.html', error=3)

        # Ensure that confirmation and password was submitted
        elif not password and not confirmation:
            return render_template('register.html', error=4)

        # Ensure username was submitted
        elif not username:
            return render_template('register.html', error=5)

        # Ensure password was submitted
        elif not password:
            return render_template('register.html', error=6)

        # Ensure that password was submitted
        elif not confirmation:
            return render_template('register.html', error=7)

        # If the user already exists
        if len(rows) != 0:
            return render_template('register.html', error=8)

        # Ensure that password and confirmation match and that user was submitted
        elif password != confirmation and not username and password:
            return render_template('register.html', error=9)

        # Ensure that password and confirmation match and that user was submitted
        elif password != confirmation and username and password:
            return render_template('register.html', error=10)

        # Ensure that password and confirmation match
        elif password != confirmation and password:
            return render_template('register.html', error=11)

        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure that username and password was submitted
        if not username and not password:
            return render_template('login.html', error=1)

        # Ensure that password was submitted
        elif not password:
            return render_template('login.html', error=2)

        # Ensure that username was submitted
        elif not username:
            return render_template('login.html', error=3)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template('login.html', error=4)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = request.form.get("username")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/home")
@login_required
def home():
    return render_template('home.html', upload=0)


@app.route('/uploader', methods = ['POST'])
@login_required
def upload_file():
    if request.method == 'POST':

        image = request.files['image']
        audio = request.files['audio']

        # Ensure that image was submitted
        if not image and not audio:
            flash('No selected file')
            return render_template("home.html", error=1, upload=0)
        elif not image:
            return render_template("home.html", error=2, upload=0)
        elif not audio:
            return render_template("home.html", error=3, upload=0)

        imagename = secure_filename('image')
        imagepath = os.path.join(app.config['UPLOAD_FOLDER'], imagename)
        image.save(imagepath)

        audioname = secure_filename('audio')
        audiopath = os.path.join(app.config['UPLOAD_FOLDER'], audioname)
        audio.save(audiopath)

        name = 'video.mp4'
        videopath = os.path.join(app.config['RESULTS_FOLDER'], name)
        add_static_image_to_audio(imagepath, audiopath, videopath)

        return redirect("/get-video/video.mp4")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/get-video/<path:video_name>")
@login_required
def get_video(video_name):
	 try:
	 	return send_from_directory(app.config['RESULTS_FOLDER'], video_name, as_attachment=True, conditional=False)
	 except FileNotFoundError:
	 	abort(404)