import json
from functools import wraps

from flask import Blueprint, Response
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from src import apology
from src.db import get_db

bp = Blueprint("admin", __name__)


def admin_required(f):
    """
    Decorate routes to require admin access.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin") is None:
            return apology("not found", 404)
        return f(*args, **kwargs)

    return decorated_function


@bp.route("/admin/settings")
@admin_required
def admin_settings():
    """ Admin panel - settings"""
    if request.method == "GET":
        # Get setting query
        db = get_db()
        settings = db.execute("SELECT * FROM settings").fetchone()

        return render_template("/admin/settings.html", settings=settings)

    return apology("Method Not Allowed", 405)


@bp.route("/admin/settings/global", methods=["POST"])
@admin_required
def admin_settings_global():
    """ Admin panel - settings global"""
    if request.method == "POST":
        settings = request.form
        # Update the settings
        db = get_db()
        db.execute("UPDATE settings SET 'store_name' = ?, 'footer_desc' = ? WHERE id = 1", (settings['store_name'], settings['footer_desc']))
        db.commit()

        return redirect("/admin/settings")

    return apology("Method Not Allowed", 405)


@bp.route("/admin/settings/main", methods=["POST"])
@admin_required
def admin_settings_main():
    """ Admin panel - settings main page"""
    if request.method == "POST":
        settings = request.form
        # Update the settings
        db = get_db()
        db.execute("UPDATE settings SET 'main_header' = ?, 'main_desc' = ? WHERE id = 1", (settings['main_header'], settings['main_desc']))
        db.commit()

        return redirect("/admin/settings")

    return apology("Method Not Allowed", 405)


@bp.route("/admin/settings/contacts", methods=["POST"])
@admin_required
def admin_settings_contacts():
    """ Admin panel - settings contacts page"""
    if request.method == "POST":
        settings = request.form
        # Update the settings
        db = get_db()
        db.execute("UPDATE settings SET 'phone' = ?, 'email' = ?, 'address' = ? WHERE id = 1",
                   (settings['phone'], settings['email'], settings['address']))
        db.commit()

        return redirect("/admin/settings")

    return apology("Method Not Allowed", 405)


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
        db.execute("UPDATE user SET username = ?, "
                   + "fullname = ?, "
                   + "phone = ?, "
                   + "email = ?, "
                   + "address = ?, "
                   + "is_admin = ?"
                   + " WHERE id = ?",
                   (user['username'], user['fullname'], user['phone'], user['email'], user['address'], is_admin,
                    user['id'])
                   )
        db.commit()

        flash("User data edited successfully")
        return redirect("/admin/users")

    return apology("Method Not Allowed", 405)
