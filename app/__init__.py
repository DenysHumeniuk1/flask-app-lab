import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lab4-local-development-key-change-me')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

from . import views
from .users import user_bp
from .products import products_bp
app.register_blueprint(user_bp)
app.register_blueprint(products_bp, url_prefix='/products')
