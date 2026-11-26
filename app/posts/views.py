from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import select

from . import post_bp
from .models import Post, User, Tag
from .forms import PostForm
from ..extensions import db


def configure_post_form(form):
    authors = db.session.scalars(select(User).order_by(User.id)).all()
    tags = db.session.scalars(select(Tag).order_by(Tag.name)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    return authors, tags


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    authors, tags = configure_post_form(form)

    if not authors:
        flash("Спочатку додайте хоча б одного автора через flask shell.", "warning")
        return render_template(
            "posts/add_post.html", title="Додати пост", form=form,
            heading="Додати пост", has_authors=False,
        )

    if form.validate_on_submit():
        author = db.session.get(User, form.author_id.data)
        selected_tags = db.session.scalars(
            select(Tag).where(Tag.id.in_(form.tags.data or []))
        ).all()
        post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            category=form.category.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data or datetime.utcnow(),
            user=author,
            tags=selected_tags,
        )
        db.session.add(post)
        db.session.commit()
        flash("Публікацію успішно додано", "success")
        return redirect(url_for("posts.post_list"))

    return render_template(
        "posts/add_post.html", title="Додати пост", form=form,
        heading="Додати пост", has_authors=True,
    )


@post_bp.route("", methods=["GET"])
@post_bp.route("/", methods=["GET"])
def post_list():
    posts = db.session.scalars(
        select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    ).all()
    return render_template("posts/posts.html", title="Усі пости", posts=posts)


@post_bp.route("/<int:post_id>")
def post_detail(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template("posts/detail_post.html", title=post.title, post=post)


@post_bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)
    configure_post_form(form)

    if request.method == "GET":
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        author = db.session.get(User, form.author_id.data)
        selected_tags = db.session.scalars(
            select(Tag).where(Tag.id.in_(form.tags.data or []))
        ).all()
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data or post.posted
        post.user = author
        post.tags = selected_tags
        db.session.commit()
        flash("Публікацію успішно оновлено", "success")
        return redirect(url_for("posts.post_detail", post_id=post.id))

    return render_template(
        "posts/add_post.html", title="Редагувати пост", form=form,
        heading="Редагувати пост", post=post, has_authors=True,
    )


@post_bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Публікацію видалено", "success")
        return redirect(url_for("posts.post_list"))
    return render_template("posts/delete_confirm.html", title="Видалити пост", post=post)
