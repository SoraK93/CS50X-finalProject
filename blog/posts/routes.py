from blog import db
from blog.posts.forms import CreatePostForm, CommentForm
from blog.models import Post, Comment
from flask import flash, render_template, redirect, request, url_for, abort, Blueprint
from flask_login import login_required, current_user

posts = Blueprint("posts", __name__)

@posts.route("/post", methods=["GET", "POST"])
@login_required
def post():
	form = CreatePostForm()
	if form.validate_on_submit():
		new_post = Post(
			title=form.heading.data,
			description=form.description.data,
			post_image=form.post_image.data,
			content=form.content.data,
			author=current_user
		)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for("main.home"))
	return render_template("create_post.html", form=form, value="Create")


@posts.route("/update_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
	form = CreatePostForm()
	post = db.session.execute(db.select(Post).where(Post.id==post_id)).scalar_one_or_none()
	if post is None:
		abort(404)
	if current_user.id != post.author_id:
		abort(401)
	if form.validate_on_submit():
		post.title = form.heading.data
		post.description = form.description.data
		post.post_image = form.post_image.data
		post.content = form.content.data
		db.session.commit()
		flash("Your post has been updated", "success")
		return redirect(url_for("posts.show_post", post_id=post.id))
	form.heading.data = post.title
	form.description.data = post.description
	form.post_image.data = post.post_image
	form.content.data = post.content
	return render_template("create_post.html", form=form, post=post, value="Update")


@posts.route("/delete_post/<int:post_id>")
@login_required
def delete_post(post_id):
	post = db.session.execute(db.select(Post).where(Post.id==post_id)).scalar()
	if current_user.id != post.author_id:
		abort(401)
	db.session.delete(post)
	db.session.commit()
	flash("Your post has been successfully deleted", "success")
	return redirect(url_for("main.home"))


@posts.route("/show_post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
	post = db.session.execute(db.select(Post).where(Post.id==post_id)).scalar()
	if not post:
		flash("Invalid input provided.", "warning")
		return redirect(url_for("main.home"))
	form = CommentForm()
	comment_page = request.args.get("page", 1, type=int)
	comments = db.paginate(db.select(Comment).where(Comment.post_id==post_id), page=comment_page, per_page=5)
	if form.validate_on_submit():
		new_comment = Comment(
			description=form.comment.data,
			user=current_user,
			feedback=post
		)
		db.session.add(new_comment)
		db.session.commit()
		return redirect(url_for("posts.show_post", post_id=post.id))
	return render_template("post.html", post=post, date=post.date_posted.strftime("%Y-%m-%d"), form=form, comments=comments)
