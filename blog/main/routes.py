from blog import db, login_manager
from blog.models import User, Post
from flask import render_template, request, Blueprint

main = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(user_id):
	return db.get_or_404(User, user_id)


@main.route("/")
def home():
	page = request.args.get("page", 1, type=int)
	posts = db.paginate(db.select(Post).order_by(Post.date_posted.desc()), page=page, per_page=5)
	return render_template("home.html", pagetitle="HomePage", posts=posts)


@main.route("/about")
def about():
	return render_template("about.html")


@main.route("/contact")
def contact():
	return render_template("contact.html")


@main.route("/filter_post/<name>")
def filter_post(name):
	user_data = db.session.execute(db.select(User).where(User.username==name)).scalar()
	page = request.args.get("page", 1, type=int)
	get_single_users_posts = db.paginate(db.select(Post).filter_by(author_id=user_data.id).order_by(Post.date_posted.desc()), page=page, per_page=5)
	return render_template("home.html", posts=get_single_users_posts, filter=True, name=name)
