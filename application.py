import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session, make_response, logging
from flask_session import Session
from flask_cors import CORS, cross_origin
import datetime
import numpy as np
import json
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, get_GPS
from models import usersDB, messageDB, addressesDB

# Configure application
app = Flask(__name__)

# listen for CORS issue with map
# logging.getLogger('flask_cors').level = logging.DEBUG

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CORS
cors = CORS(app, resources={r"/": {"origins": "http://localhost:port"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers["Set-Cookie"] = "HttpOnly; promo_shown=1; SameSite=Lax; Max-Age=604800"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
dbb = sqlite3.connect("claims.db")
db = dbb.cursor()
# connect.execute('INSERT INTO users (username, hash) VALUES (?, ?)')
db.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL);")
db.execute("CREATE TABLE IF NOT EXISTS 'messages' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' INTEGER NOT NULL, 'title' TEXT NOT NULL, 'message' MEDIUMTEXT NOT NULL, 'file' VARCHAR(255), 'addresse_id' INTEGER NOT NULL,'category' TEXT NOT NULL, FOREIGN KEY('user_id') REFERENCES 'users'('id'), FOREIGN KEY('addresse_id') REFERENCES 'addresses'('id'));")
db.execute("CREATE TABLE IF NOT EXISTS 'addresses' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'addresse' TEXT NOT NULL, 'latitude' VARCHAR(64) NOT NULL, 'longitude' VARCHAR(64) NOT NULL, 'organization' TEXT);")

# Make sure API key is set
'''if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")'''


@app.route("/", methods=["GET"])
@login_required
@cross_origin(origin='localhost', allow_headers=['Content-Type'])
def index():
    """index, map with points of claims"""

    user_id = session["user_id"]
    with sqlite3.connect('claims.db') as conn:
        adb = addressesDB(conn)
        tpls = adb.getAllAddresses()
        points = [list(tpl) for tpl in tpls]
        # save and convert data to json if data will be parsed in js, not as python object, not by jinja reader
        # Todo: stringify also other data response which you get from sqlite and parse it in js/jinja file.
        points = json.dumps(points)
        print(f'!!!Address: {points}')
    response = make_response(render_template("map.html", points=points))

    # ignore warning on localhost about SameSite - it will work with https
    response.headers["Set-Cookie"] = "sessionId=user_id; HttpOnly; SameSite=None; Secure"
    return response

@app.route("/add",  methods=["GET", "POST"])
@login_required
def add():
    """Form add message"""
    user_id = session["user_id"]
    options = np.array(['Alert COVID', 'Bruit/Bagarre', 'Cadavre', 'Clochard',
                        'Graffiti', 'Mobilier urbain', 'Nid-de-poule', 'Propreté',
                        'Trottoir glissant', 'Zone dangereuse', 'Zone de construction'])

    if request.method == "POST":
        if not (request.form.get("title") and request.form.get("message")
                and request.form.get("city") and request.form.get("address")):
            return apology("you should fill all required* fields of form", 401)

        gps = get_GPS(request.form.get("city"), request.form.get("address"))
        if not gps:
            return apology("The address doesn't exist", 403)

        with sqlite3.connect('claims.db') as conn:
            latitude = gps.get('lat')
            longitude = gps.get('lon')
            address = request.form.get("address")
            # replace NULL by "None"
            organization = request.form.get("company")
            if organization == '':
                organization = "None"
            adb = addressesDB(conn)
            adb.add_address(latitude=latitude, longitude=longitude, address=address, organization=organization)

            mb = messageDB(user_id, conn)
            mb.add_message(address, title=request.form.get("title"), category=request.form.get("category"),
                           message=request.form.get("message"), file=request.form.get("file"))
        #   4) write function in .route("/claims") to display all added addresses in Montreal area
        return redirect("/claims")
    else:
        return render_template("add.html", action="/add", options=options)


@app.route("/claims")
@login_required
def claims():
    """List of claims"""
    user_id = session["user_id"]

    with sqlite3.connect('claims.db') as conn:
        mdb = messageDB(user_id, conn)
        messages = mdb.get_messages()
        print(f'Messages {messages}')
        return render_template("listClaims.html", messages=messages)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 401)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 402)
        '''Todo: rewrite it with set_id'''
        # Query database for username
        db.execute("SELECT * FROM users WHERE username = :username", {"username": request.form.get("username")})
        # rows = db.fetchall() #[(1, 'Fred', 'pbkdf2:sha256:150000$T7JKIKJn$076d0cb229398ad3c5340b858aaea6a636c41e6ca85359a046f83489d6eb386c')]
        rows = db.fetchone()
        if not rows:
            return apology("error, this user doesn't exist", 404)
        # Ensure username exists and password is correct, use count() instead len() to define length for sqlite3.Cursor object
        if len(rows) == 0 or not check_password_hash(rows[2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
     # Forget any user_id
    session.clear()

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was sent
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("you should provide username", 403)

        # Ensure password was sent
        elif not password:
            return apology("you should provide password", 403)

        elif not request.form.get("confirmation") or password != request.form.get("confirmation"):
            return apology("you should confirm password", 403)

        with sqlite3.connect('claims.db') as conn:
            # INSERT the new user into users db
            hash = generate_password_hash(password)
            u_db = usersDB(conn)
            u_db.register_user(username, hash)

        # Redirect user to add form
        return redirect("/")
    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return [e.name, e.code]


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
