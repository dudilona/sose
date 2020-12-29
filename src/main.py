from flask import Blueprint, session
from flask import render_template

from src.db import get_db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Show home page"""
    session['page'] = "home"
    return render_template("home.html")


@bp.route("/catalog")
def catalog():
    """Show catalog"""
    db = get_db()
    products = db.execute("SELECT * FROM product").fetchall()

    session['page'] = "catalog"
    return render_template("catalog.html", products=products)


@bp.route("/products/<int:product_id>")
def product(product_id):
    """Show product"""
    db = get_db()
    prod = db.execute("SELECT * FROM product WHERE id = ?", (product_id,)).fetchone()

    session['page'] = "catalog"
    return render_template("product.html", product=prod)


@bp.route("/contacts")
def contacts():
    """Show home page"""
    session['page'] = "contacts"
    return render_template("contacts.html")
