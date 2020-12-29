from flask import Blueprint, session
from flask import render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Show home page"""
    session['page'] = "home"
    return render_template("home.html")


@bp.route("/contacts")
def contacts():
    """Show home page"""
    session['page'] = "contacts"
    return render_template("contacts.html")
