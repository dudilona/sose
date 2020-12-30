from flask import render_template, current_app


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def allowed_file(filename):
    """Check the file extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_IMG_EXTENSIONS"]


def items_count(cart_items):
    """Calculate total items count in the cart"""
    count = 0
    if cart_items is not None:
        for item in cart_items:
            count = count + item['pieces']

    return count


def get_total_price(cart_items):
    """Calculate total price for cart items"""
    price = 0
    if cart_items is not None:
        for item in cart_items:
            price = price + item['price']

    return price
