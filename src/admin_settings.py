import os
from functools import wraps

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from src import UPLOAD_IMG_FOLDER
from src import apology
from src.db import get_db
from src.helpers import allowed_file

bp = Blueprint("admin_settings", __name__)


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
        session['page'] = "admin"
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

        # File upload
        file = request.files['favicon']
        if file and allowed_file(file.filename):
            filename = "favicon.ico"
            file.save(os.path.join(UPLOAD_IMG_FOLDER, filename))

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

        # File upload
        file = request.files['main_image_input']
        if file and allowed_file(file.filename):
            filename = "home.jpg"
            file.save(os.path.join(UPLOAD_IMG_FOLDER, filename))

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
        db.execute("UPDATE settings SET 'phone' = ?, 'email' = ?, 'address' = ?, 'google_map' = ? WHERE id = 1",
                   (settings['phone'], settings['email'], settings['address'], settings['google_map']))
        db.commit()

        return redirect("/admin/settings")

    return apology("Method Not Allowed", 405)
