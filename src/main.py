import json

from flask import Blueprint, session, request, Response
from flask import render_template

from src import apology
from src.db import get_db
from src.helpers import items_count

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
    product_item = db.execute("SELECT * FROM product WHERE id = ?", (product_id,)).fetchone()

    session['page'] = "catalog"
    return render_template("product.html", product=product_item)


@bp.route("/cart", methods=["GET", "POST", "DELETE"])
def cart():
    """Show cart"""
    if request.method == "GET":
        cart_items = []
        if session.get("cart"):
            cart_items = session.get("cart")

        total_items = 0
        total_price = 0

        for cart_item in cart_items:
            total_items = total_items + cart_item['pieces']
            total_price = total_price + (cart_item['price'] * cart_item['pieces'])

        session['page'] = "cart"
        return render_template("cart.html", cart_items=cart_items, total_items=total_items, total_price=total_price)

    """Add the product to the cart"""
    if request.method == "POST":
        data = json.loads(request.data)
        product_id = data['product_id']
        pieces = data['pieces']

        db = get_db()
        product_item = db.execute("SELECT * FROM product WHERE id = ?", (product_id,)).fetchone()

        cart_items = []
        if session.get("cart"):
            cart_items = session.get("cart")
        cart_item = dict(product_item)
        cart_item['pieces'] = pieces
        cart_item['total'] = pieces * cart_item['price']
        cart_item['product_id'] = product_item['id']
        cart_item['id'] = len(cart_items)
        cart_items.append(cart_item)
        session['cart'] = cart_items

        session['cart_total_items'] = items_count(cart_items)

        return Response(status=200)

    """Delete the cart item from the cart"""
    if request.method == "DELETE":

        item_id = json.loads(request.data)['item_id']

        session['cart'] = [item for item in session['cart'] if not item['id'] == item_id]

        session['cart_total_items'] = items_count(session['cart'])

        return Response(status=200)

    return apology("Method Not Allowed", 405)


@bp.route("/contacts")
def contacts():
    """Show home page"""
    session['page'] = "contacts"
    return render_template("contacts.html")
