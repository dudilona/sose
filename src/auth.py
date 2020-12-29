from functools import wraps

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from src import apology
from src.db import get_db

bp = Blueprint("auth", __name__)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        session['page'] = "register"
        return render_template("auth/register.html")

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
        db = get_db()
        rows = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchall()
        # Check that the username is unique
        if len(rows) > 0:
            return apology("This username already exists", 400)

        # Check passwords are equal
        if password != password2:
            return apology("The passwords aren't equal", 400)

        # Query database for admin - first user will be admin
        rows = db.execute("SELECT * FROM user").fetchall()
        is_admin = 0
        if len(rows) == 0:
            is_admin = 1

        # Create the user in the data base
        pass_hash = generate_password_hash(password)
        user_id = db.execute("INSERT INTO user (username, hash, fullname, phone, email, address, is_admin) "
                             "VALUES (?, ?, ?, ?, ?, ?, ?)"
                             , (username, pass_hash, fullname, phone, email, address, is_admin),
                             ).lastrowid
        db.commit()

        # Remember which user has logged in
        session["user_id"] = user_id
        session['username'] = username
        if is_admin == 1:
            session["admin"] = user_id

        # Redirect user to home page
        flash('Registered!')
        return redirect("/")

    return apology("Method Not Allowed", 405)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        session['page'] = "login"
        return render_template("auth/login.html")

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
        db = get_db()
        rows = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session['username'] = username
        if rows[0]["is_admin"] == 1:
            session["admin"] = rows[0]["id"]

        # Redirect user to home page
        flash(username + ', welcome!')
        return redirect("/")


@bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
