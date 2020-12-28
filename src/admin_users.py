import json

from flask import Blueprint, Response
from flask import flash
from flask import redirect
from flask import render_template
from flask import request

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
