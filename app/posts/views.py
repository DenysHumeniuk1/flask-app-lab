from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort, request, session
from . import post_bp
from .models import Post
from .forms import PostForm
from ..extensions import db

@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            category=form.category.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data or datetime.utcnow(),
            author=(session.get("username") or "Anonymous")[:20],
        )
        db.session.add(post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.post_list"))
    return render_template("posts/add_post.html", title="Додати пост", form=form, heading="Додати пост")

@post_bp.route("", methods=["GET"])
@post_bp.route("/", methods=["GET"])
def post_list():
    posts = db.session.execute(
        db.select(Post).where(Post.is_active.is_(True)).order_by(Post.posted.desc())
    ).scalars().all()
    return render_template("posts/posts.html", title="Усі пости", posts=posts)

@post_bp.route("/<int:post_id>")
def post_detail(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template("posts/detail_post.html", title=post.title, post=post)

@post_bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)
    if request.method == "GET":
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
    if form.validate_on_submit():
        form.populate_obj(post)
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data or post.posted
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.post_detail", post_id=post.id))
    return render_template("posts/add_post.html", title="Редагувати пост", form=form, heading="Редагувати пост", post=post)

@post_bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")
        return redirect(url_for("posts.post_list"))
    return render_template("posts/delete_confirm.html", title="Видалити пост", post=post)
