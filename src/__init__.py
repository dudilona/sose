import os
from tempfile import mkdtemp

from flask import Flask
from flask_session import Session
from werkzeug.exceptions import HTTPException, InternalServerError, default_exceptions

from src.helpers import apology, usd

# Config for img files upload
UPLOAD_IMG_FOLDER = 'src/static/img'
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'ico'}


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "shop.db"),
    )

    # Config for img files upload
    app.config['UPLOAD_FOLDER'] = UPLOAD_IMG_FOLDER
    app.config['ALLOWED_IMG_EXTENSIONS'] = ALLOWED_IMG_EXTENSIONS

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Ensure responses aren't cached
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    # Listen for errors
    def errorhandler(e):
        """Handle error"""
        if not isinstance(e, HTTPException):
            e = InternalServerError()
        return apology(e.name, e.code)

    for code in default_exceptions:
        app.errorhandler(code)(errorhandler)

    # register the database commands
    from src import db

    db.init_app(app)

    # apply the blueprints to the app
    from src import auth, main, admin_users, admin_settings, admin_products, admin_orders, user

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin_settings.bp)
    app.register_blueprint(admin_users.bp)
    app.register_blueprint(admin_products.bp)
    app.register_blueprint(admin_orders.bp)
    app.register_blueprint(user.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    @app.context_processor
    def inject_settings_variables():
        settings = db.get_db().execute("SELECT * FROM settings WHERE id = 1").fetchone()
        return dict(settings=dict(settings))

    app.jinja_env.filters["usd"] = usd

    return app


if __name__ == '__main__':
    create_app().run()
