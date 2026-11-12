import logging
import os
from flask import render_template, request, redirect, url_for, flash, current_app
from .forms import ContactForm

def register_main_routes(app):
    log_path = os.path.join(app.root_path, "contact.log")
    contact_logger = logging.getLogger("contact_form")
    contact_logger.setLevel(logging.INFO)
    if not any(getattr(handler, "baseFilename", None) == os.path.abspath(log_path)
               for handler in contact_logger.handlers):
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        contact_logger.addHandler(handler)

    @app.route("/")
    @app.route("/resume")
    def resume():
        return render_template("resume.html", title="Резюме")

    @app.route("/contacts", methods=["GET", "POST"])
    @app.route("/contact", methods=["GET", "POST"])
    def contacts():
        form = ContactForm()
        if form.validate_on_submit():
            try:
                contact_logger.info(
                    "Contact submitted: name=%r email=%r phone=%r subject=%r message=%r",
                    form.name.data, form.email.data, form.phone.data,
                    form.subject.data, form.message.data
                )
                flash("Повідомлення успішно надіслано та записано.", "success")
            except OSError:
                current_app.logger.exception("Не вдалося записати контактне повідомлення")
                flash("Не вдалося записати повідомлення. Спробуйте ще раз.", "danger")
            return redirect(url_for("contacts"))
        return render_template("contacts.html", title="Контакти", form=form)

    @app.route("/homepage")
    def home():
        return render_template("homepage.html", title="Головна", agent=request.user_agent)
