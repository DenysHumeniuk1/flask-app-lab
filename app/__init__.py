import os
from flask import Flask

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "lab5-local-development-key"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    UPLOAD_FOLDER=os.path.join(app.root_path, "products", "static", "uploads"),
)

from . import views
from .users import user_bp
from .products import products_bp
app.register_blueprint(user_bp)
app.register_blueprint(products_bp)
