from datetime import datetime, timezone
from flask import render_template, request, redirect, url_for, flash, make_response
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import select

from . import user_bp
from .forms import RegistrationForm, LoginForm
from ..extensions import db
from ..posts.models import User


COOKIE_PREFIX = "lab4_"


@user_bp.route("/hi/<name>")
def greetings(name):
    age = request.args.get("age", type=int)
    return render_template("users/hi.html", title="Привітання", name=name, age=age)


@user_bp.route("/admin")
def admin():
    return redirect(url_for("users.greetings", name="administrator", age=45))


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Реєстрація успішна! Ви увійшли в систему.", "success")
        return redirect(url_for("users.account"))
    return render_template("users/register.html", title="Реєстрація", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.email == form.email.data.strip().lower()))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Вхід успішний!", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)
            return redirect(url_for("users.account"))
        flash("Неправильна електронна адреса або пароль.", "danger")
    return render_template("users/login.html", title="Вхід", form=form)


@user_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))


@user_bp.route("/account")
@user_bp.route("/profile")
@login_required
def account():
    cookies = {k: v for k, v in request.cookies.items() if k.startswith(COOKIE_PREFIX)}
    theme = request.cookies.get("lab4_theme", "light")
    if theme not in ("light", "dark"):
        theme = "light"
    return render_template(
        "users/profile.html", title="Профіль", username=current_user.username,
        cookies=cookies, theme=theme,
    )


@user_bp.route("/all")
@login_required
def all_users():
    users = db.session.scalars(select(User).order_by(User.id)).all()
    return render_template("users/all_users.html", title="Усі користувачі", users=users, user_count=len(users))


@user_bp.route("/cookies/add", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    try:
        age = int(request.form.get("max_age", "3600"))
    except ValueError:
        age = 0
    if not key or not key.replace("_", "").isalnum() or len(key) > 40 or age < 1 or age > 31536000:
        flash("Ключ: лише літери, цифри й _. Термін: 1–31536000 секунд.", "danger")
        return redirect(url_for("users.account"))
    if key == "theme" or len(value) > 1000:
        flash("Недопустимий ключ або занадто довге значення.", "danger")
        return redirect(url_for("users.account"))
    response = make_response(redirect(url_for("users.account")))
    response.set_cookie(COOKIE_PREFIX + key, value, max_age=age, httponly=True, samesite="Lax")
    flash("Кукі успішно додано.", "success")
    return response


@user_bp.route("/cookies/delete", methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key", "").strip()
    response = make_response(redirect(url_for("users.account")))
    if key and key != "theme" and COOKIE_PREFIX + key in request.cookies:
        response.delete_cookie(COOKIE_PREFIX + key)
        flash("Кукі видалено.", "success")
    else:
        flash("Кукі не знайдено або ключ недоступний.", "warning")
    return response


@user_bp.route("/cookies/delete-all", methods=["POST"])
@login_required
def delete_all_cookies():
    response = make_response(redirect(url_for("users.account")))
    for key in request.cookies:
        if key.startswith(COOKIE_PREFIX):
            response.delete_cookie(key)
    flash("Усі кукі лабораторної видалено.", "success")
    return response


@user_bp.route("/theme/<theme>", methods=["POST"])
@login_required
def change_theme(theme):
    if theme not in ("light", "dark"):
        flash("Невідома тема.", "danger")
        return redirect(url_for("users.account"))
    response = make_response(redirect(url_for("users.account")))
    response.set_cookie("lab4_theme", theme, max_age=31536000, httponly=True, samesite="Lax")
    flash("Тему змінено.", "success")
    return response
