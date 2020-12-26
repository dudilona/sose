from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Add access to function from templates
app.jinja_env.globals.update(usd=usd)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shop.db")


@app.route("/")
def index():
    """Show home page"""
    return render_template("home.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        fullname = request.form.get("fullname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")

        # Ensure required fields was submitted
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if not password2:
            return apology("must provide password2", 400)
        if not fullname:
            return apology("must provide fullname", 400)
        if not phone:
            return apology("must provide phone", 400)
        if not email:
            return apology("must provide email", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE username = :username", username=username)
        # Check that the username is unique
        if len(rows) > 0:
            return apology("This username already exists", 400)

        # Check passwords are equal
        if password != password2:
            return apology("The passwords aren't equal", 400)

        # Create the user in the data base
        passHash = generate_password_hash(password)
        userId = db.execute("INSERT INTO user (username, hash, fullname, phone, email, address) "
                   "VALUES (:username, :hash, :fullname, :phone, :email, :address)"
                   , username=username, hash=passHash, fullname=fullname, phone=phone, email=email, address=address)

        # Remember which user has logged in
        session["user_id"] = userId

        # Redirect user to home page
        flash('Registered!')
        return redirect("/")

    return apology("Method Not Allowed", 405)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash(username + ', welcome!')
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
