import json
import os

from flask import Blueprint, Response, redirect
from flask import flash
from flask import render_template
from flask import request

from src import apology, UPLOAD_IMG_FOLDER
from src.admin_settings import admin_required
from src.db import get_db
from src.helpers import allowed_file

bp = Blueprint("admin_products", __name__)


@bp.route("/admin/products", methods=["GET", "DELETE"])
@admin_required
def admin_products():
    """ Admin panel - products"""
    if request.method == "GET":
        # Get all products
        db = get_db()
        products = db.execute("SELECT * FROM product").fetchall()

        return render_template("admin/products.html", products=products)

    if request.method == "DELETE":
        # Delete the product from database
        product_id = json.loads(request.data)['productId']
        db = get_db()
        db.execute("DELETE FROM product WHERE id = ?", (product_id,))
        db.commit()

        flash("The product deleted")
        return Response(status=200)

    return apology("Method Not Allowed", 405)


@bp.route("/admin/products/add", methods=["GET", "POST"])
@admin_required
def admin_products_add():
    """ Admin panel - add new products"""
    if request.method == "GET":
        return render_template("admin/product-add.html")

    if request.method == "POST":
        product = request.form
        # Add new product
        db = get_db()
        product_id = db.execute("INSERT INTO product (name, price, header, instruction, info)"
                                "VALUES (?, ?, ?, ?, ?)",
                                (product['name'], product['price'], product['header'], product['instruction'], product['info'])).lastrowid
        db.commit()

        # File upload
        file = request.files['product_image_input']
        if file and allowed_file(file.filename):
            filename = "product" + str(product_id) + ".png"
            file.save(os.path.join(UPLOAD_IMG_FOLDER + "/products", filename))
        flash("Product added successfully")
        return redirect("/admin/products")

    return apology("Method Not Allowed", 405)
