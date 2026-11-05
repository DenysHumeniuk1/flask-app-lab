import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from tinydb import TinyDB
from flask import render_template, redirect, url_for, flash, abort, current_app, request
from werkzeug.utils import secure_filename
from . import products_bp
from ..forms import ProductForm, DeleteForm

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "products.json")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
db = TinyDB(DB_PATH)
products_table = db.table("products")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def save_image(file):
    if not file or not file.filename:
        return None
    original = secure_filename(file.filename)
    ext = original.rsplit(".", 1)[-1].lower() if "." in original else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Дозволені лише PNG, JPG та JPEG.")
    filename = f"{uuid.uuid4().hex}.{ext}"
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    file.save(os.path.join(folder, filename))
    return filename

def get_product(product_id):
    return products_table.get(lambda item: item.get("id") == product_id)

def list_products():
    return sorted(products_table.all(), key=lambda item: item.get("id", 0))

@products_bp.route("/product", methods=["GET"])
@products_bp.route("/products/", methods=["GET"])
def product_list():
    return render_template("products/products.html", title="Товари", products=list_products())

@products_bp.route("/product/<int:product_id>")
@products_bp.route("/products/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)
    return render_template("products/detail_product.html", title=product["name"], product=product, delete_form=DeleteForm())

@products_bp.route("/product/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        try:
            image = save_image(form.image.data)
            next_id = max((item["id"] for item in products_table.all()), default=0) + 1
            product = {
                "id": next_id, "name": form.name.data.strip(),
                "content": form.content.data.strip(), "price": str(Decimal(form.price.data).quantize(Decimal("0.01"))),
                "category": form.category.data, "quantity": form.quantity.data,
                "image": image, "created_at": datetime.now(timezone.utc).isoformat()
            }
            products_table.insert(product)
            flash("Товар успішно додано.", "success")
            return redirect(url_for("products.product_detail", product_id=next_id))
        except (OSError, ValueError):
            current_app.logger.exception("Product creation failed")
            flash("Не вдалося зберегти товар або зображення.", "danger")
    return render_template("products/product_form.html", title="Додати товар", form=form, heading="Додати товар")

@products_bp.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)
    form = ProductForm()
    if request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = Decimal(str(product["price"]))
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]
    if form.validate_on_submit():
        try:
            new_image = save_image(form.image.data)
            updated = {
                "name": form.name.data.strip(), "content": form.content.data.strip(),
                "price": str(Decimal(form.price.data).quantize(Decimal("0.01"))),
                "category": form.category.data, "quantity": form.quantity.data,
                "image": new_image or product.get("image")
            }
            products_table.update(updated, lambda item: item.get("id") == product_id)
            flash("Зміни товару збережено.", "success")
            return redirect(url_for("products.product_detail", product_id=product_id))
        except (OSError, ValueError):
            current_app.logger.exception("Product update failed")
            flash("Не вдалося зберегти зміни.", "danger")
    return render_template("products/product_form.html", title="Редагувати товар", form=form, heading="Редагувати товар", product=product)

@products_bp.route("/product/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Не вдалося підтвердити видалення. Оновіть сторінку та спробуйте ще раз.", "danger")
        return redirect(url_for("products.product_detail", product_id=product_id))
    products_table.remove(lambda item: item.get("id") == product_id)
    flash("Товар видалено.", "success")
    return redirect(url_for("products.product_list"))
