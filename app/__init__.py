
import os
from flask import Flask, render_template
from .config import config
from .extensions import db, migrate, csrf


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)

    config_name = config_name or os.environ.get(
        "FLASK_ENV", "development"
    )

    app.config.from_object(
        config.get(config_name, config["development"])
    )

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from . import models
    from .users import user_bp
    from .products import products_bp
    from .posts import post_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(post_bp)

    from .views import register_main_routes
    register_main_routes(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app