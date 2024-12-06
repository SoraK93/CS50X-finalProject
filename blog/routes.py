from blog import app, bcrypt, db, login_manager
from blog.models import User, Post
from flask import flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf.form import Form
from blog.forms import RegistrationForm, LoginForm, CreatePostForm


@login_manager.user_loader
def load_user(user_id):
	return db.get_or_404(User, user_id)


@app.route("/")
def home():
	posts = db.session.execute(db.select(Post)).scalars()
	return render_template("home.html", pagetitle="HomePage", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		new_user = User(
			username=form.username.data,
			email=form.email.data,
			password=hashed_password
		)
		db.session.add(new_user)
		db.session.commit()
		flash(message="You have registered successfully", category="success")
		return redirect(url_for("login"))
	return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	
	if form.validate_on_submit():
		email = form.email.data
		user = db.session.execute(db.select(User).where(User.email==email)).scalar()
		if user:
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				return redirect(url_for("home"))
			else:
				flash("Incorrect Email/ Password provided. Please check user credentials.", "danger")
				return redirect(url_for("login"))	
		else:
			flash("User not registered. Please register here.", "warning")
			return redirect(url_for("register"))
	return render_template("login.html", form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/contact")
def contact():
	return render_template("contact.html")


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
	form = CreatePostForm()
	if form.validate_on_submit():
		new_post = Post(
			title = form.heading.data,
			description = form.description.data,
			content = form.content.data,
			author = current_user
		)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for("home"))
	return render_template("create_post.html", form=form)


@app.route("/update_post/<int:post_id>", methods=["GET", "POST"])
def update_post(post_id):
	form = CreatePostForm()
	post = db.session.execute(db.select(Post).where(Post.id==post_id)).scalar()
	if form.validate_on_submit():
		post.title = form.heading.data
		post.description = form.description.data
		post.content = form.content.data
		db.session.commit()
		flash("Your post has been updated", "success")
		return redirect(url_for("home"))
	form.heading.data = post.title
	form.description.data = post.description
	form.content.data = post.content
	return render_template("create_post.html", form=form, post=post, update=True)