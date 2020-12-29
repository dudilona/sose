import json

from flask import Blueprint, Response
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

from src import apology
from src.auth import login_required
from src.db import get_db

bp = Blueprint("user", __name__)


@bp.route("/user/edit", methods=["GET", "POST"])
@login_required
def user_edit():
    """ User panel - user edit"""
    if request.method == "GET":
        session['page'] = "user"
        user_id = session['user_id']
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

        return render_template("user/user-edit.html", user=user)

    if request.method == "POST":
        user = request.form

        db = get_db()
        db.execute("UPDATE user SET "
                   "username = ?, "
                   "fullname = ?, "
                   "phone = ?, "
                   "email = ?, "
                   "address = ? "
                   "WHERE id = ?",
                   (user['username'], user['fullname'], user['phone'], user['email'], user['address'], user['id'])
                   )
        db.commit()

        # If user change his username
        session['username'] = user['username']

        flash("User data edited successfully")
        return redirect("/user/edit")

    return apology("Method Not Allowed", 405)


@bp.route("/user/password", methods=["GET", "POST"])
@login_required
def user_password():
    """ User panel - user edit password"""
    if request.method == "GET":
        user_id = request.args.get("userId")
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

        return render_template("user/user-password.html", user=user)

    if request.method == "POST":
        user_id = request.form.get("user_id")
        new_pass = request.form.get("password")
        confirm_pass = request.form.get("password2")
        current_pass = request.form.get("cur_pass")

        # Ensure newPass was submitted
        if not new_pass:
            return apology("must provide new password", 400)

        # Ensure confirmPass was submitted
        if not confirm_pass:
            return apology("must provide new password confirmation", 400)

        # Ensure current password was submitted
        if not current_pass:
            return apology("must provide current password", 400)

        # Check passwords are equal
        if new_pass != confirm_pass:
            return apology("The passwords aren't equal", 400)

        # Query database for username hash
        db = get_db()
        user_hash = db.execute("SELECT hash FROM user WHERE id = ?", (user_id,)).fetchone()['hash']

        if not check_password_hash(user_hash, current_pass):
            return apology("The current password isn't correct", 400)

        # Update the password
        db = get_db()
        db.execute("UPDATE user SET hash = ? WHERE id = ?", (generate_password_hash(new_pass), user_id), )
        db.commit()

        flash('The password is changed')
        return redirect("/user/edit?" + user_id)

    return apology("Method Not Allowed", 405)
