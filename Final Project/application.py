import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from dateutil import parser
from json import dumps, loads
from random import choice

from api_helpers import search
from helpers import apology, login_required

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter for datetime
@app.template_filter("strftime")
def _jinja2_filter_datetime(date, fmt=None):
    date = parser.parse(date)
    native = date.replace(tzinfo=None)
    format = "%d %b %y, %H:%M"
    return native.strftime(format)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///guardian-news.db")
db.execute("PRAGMA foreign_keys = ON")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        userPreferencesRecord = db.execute("SELECT preferences FROM user_preferences WHERE user_id = :user_id",
                                           user_id=session["user_id"])
        if not userPreferencesRecord:
            query = ""
        else:
            userPreferencesList = loads(
                userPreferencesRecord[0]["preferences"])
            query = choice(userPreferencesList)

        return render_template("home.html", news=search(query))

    query = request.form.get("query")
    return render_template("home.html", news=search(query))


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")

    if not request.form.get("username"):
        return apology("must provide username", 400)
    elif not request.form.get("password"):
        return apology("must provide password", 400)

    rows = db.execute("SELECT * FROM user WHERE username = :username",
                      username=request.form.get("username"))

    if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
        return apology("invalid username and/or password", 400)

    session["user_id"] = rows[0]["id"]
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    details = [request.form.get("username"), request.form.get(
        "password"), request.form.get("confirmation")]

    if not details[0]:
        return apology("must provide username", 400)
    elif not details[1]:
        return apology("must provide password", 400)
    elif not details[2]:
        return apology("must provide password confirmation", 400)
    elif details[1] != details[2]:
        return apology("password must match confirmation", 400)

    result = db.execute("INSERT INTO user (username, password) VALUES (:username, :password)",
                        username=details[0], password=generate_password_hash(details[1]))
    if not result:
        return apology("user is already registered", 400)

    flash("User Registered!")
    return redirect("/")


@app.route("/check-username", methods=["GET"])
def checkUsername():
    usernameInput = request.args.get("username")
    userRecord = db.execute(
        "SELECT * FROM user WHERE username = :usernameInput", usernameInput=usernameInput)

    usernameIsValid = userRecord == [] and len(usernameInput) >= 1
    return jsonify(usernameIsValid)


@app.route("/save-story", methods=["POST"])
@login_required
def saveStory():
    story = request.json

    existingRecord = db.execute("SELECT * FROM user_stories WHERE user_id = :user_id AND title = :title AND url = :url",
                                user_id=session["user_id"], title=story["title"], url=story["url"])
    if existingRecord:
        return jsonify(True)

    newStoryRecord = db.execute("INSERT INTO user_stories (user_id, date, section, title, url) VALUES (:user_id, :date, :section, :title, :url)",
                                user_id=session["user_id"], date=story["date"], section=story["section"], title=story["title"], url=story["url"])
    if not newStoryRecord:
        return jsonify(False)

    return jsonify(True)


@app.route("/saved-stories", methods=["GET"])
@login_required
def getStories():
    userStories = db.execute("SELECT * FROM user_stories WHERE user_id = :user_id",
                             user_id=session["user_id"])

    return render_template("saved_stories.html", stories=userStories)


@app.route("/delete-story", methods=["DELETE"])
@login_required
def deleteStory():
    if not request.json:
        return apology("must provide a story to delete", 400)

    deletedStories = db.execute("DELETE FROM user_stories WHERE id = :story_id",
                                story_id=request.json)

    return jsonify(deletedStories)


@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    if request.method == "GET":
        return render_template("preferences.html")

    preferencesList = ["art", "business", "entertainment",
                       "health", "music", "science", "sports", "other"]
    userPreferencesList = []
    newPreferences = None
    updatedPreferences = None

    for p in preferencesList:
        preference = request.form.get(p) if request.form.get(p) != "" else None
        (userPreferencesList.append(preference)
         if preference is not None else None)

    existingPreferences = db.execute("SELECT * FROM user_preferences WHERE user_id = :user_id",
                                     user_id=session["user_id"])
    if not existingPreferences:
        newPreferences = db.execute("INSERT INTO user_preferences (user_id, preferences) VALUES (:user_id, :preferences)",
                                    user_id=session["user_id"], preferences=dumps(userPreferencesList))
    else:
        updatedPreferences = db.execute("UPDATE user_preferences SET preferences = :preferences WHERE user_id = :user_id",
                                        preferences=dumps(userPreferencesList), user_id=session["user_id"])

    if not newPreferences and not updatedPreferences:
        flash("Failed to save preferences!")

    flash("Preferences saved!")
    return render_template("preferences.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
