import json

from flask import Blueprint, Response
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from werkzeug.security import generate_password_hash

from src import apology
from src.admin_settings import admin_required
from src.db import get_db

bp = Blueprint("admin_users", __name__)


@bp.route("/admin/users", methods=["GET", "DELETE"])
@admin_required
def admin_users():
    """ Admin panel - users"""
    if request.method == "GET":
        # Get all users
        db = get_db()
        users = db.execute("SELECT * FROM user").fetchall()

        return render_template("admin/users.html", users=users)

    if request.method == "DELETE":
        # Delete the user from database
        user_id = json.loads(request.data)['userId']
        db = get_db()
        db.execute("DELETE FROM user WHERE id = ?", (user_id,))
        db.commit()

        flash("User deleted")
        return Response(status=200)

    return apology("Method Not Allowed", 405)


@bp.route("/admin/users/edit", methods=["GET", "POST"])
@admin_required
def admin_users_edit():
    """ Admin panel - user edit"""
    if request.method == "GET":
        user_id = request.args.get("userId")
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

        return render_template("admin/user-edit.html", user=user)

    if request.method == "POST":
        user = request.form
        is_admin = 0
        if 'admin' in user and user['admin'] == "on":
            is_admin = 1

        db = get_db()
        db.execute("UPDATE user SET "
                   "username = ?, "
                   "fullname = ?, "
                   "phone = ?, "
                   "email = ?, "
                   "address = ?, "
                   "is_admin = ?"
                   " WHERE id = ?",
                   (user['username'], user['fullname'], user['phone'], user['email'], user['address'], is_admin, user['id'])
                   )
        db.commit()

        # If admin change him username
        if session['user_id'] == int(user['id']):
            session['username'] = user['username']

        flash("User data edited successfully")
        return redirect("/admin/users")

    return apology("Method Not Allowed", 405)


@bp.route("/admin/users/password", methods=["GET", "POST"])
@admin_required
def admin_users_password():
    """ Admin panel - user edit password"""
    if request.method == "GET":
        user_id = request.args.get("userId")
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

        return render_template("admin/user-password.html", user=user)

    if request.method == "POST":
        user_id = request.form.get("user_id")
        new_pass = request.form.get("password")
        confirm_pass = request.form.get("password2")

        # Ensure newPass was submitted
        if not new_pass:
            return apology("must provide new password", 400)

        # Ensure confirmPass was submitted
        if not confirm_pass:
            return apology("must provide new password confirmation", 400)

        # Check passwords are equal
        if new_pass != confirm_pass:
            return apology("The passwords aren't equal", 400)

        # Update the password
        db = get_db()
        db.execute("UPDATE user SET hash = ? WHERE id = ?", (generate_password_hash(new_pass), user_id), )
        db.commit()

        flash('The password is changed')
        return redirect("/admin/users/edit?userId=" + user_id)

    return apology("Method Not Allowed", 405)
