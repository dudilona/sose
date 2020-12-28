from flask import Blueprint
from flask import render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Show home page"""
    return render_template("home.html")
