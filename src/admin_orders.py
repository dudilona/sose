from flask import Blueprint
from flask import render_template
from flask import request

from src import apology
from src.admin_settings import admin_required
from src.db import get_db

bp = Blueprint("admin_orders", __name__)


@bp.route("/admin/orders")
@admin_required
def admin_orders():
    """ Admin panel - orders"""
    if request.method == "GET":
        # Get all orders
        db = get_db()
        orders = db.execute("SELECT * FROM 'order'").fetchall()

        return render_template("admin/orders.html", orders=orders)

    return apology("Method Not Allowed", 405)