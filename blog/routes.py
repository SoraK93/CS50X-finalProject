import os
import secrets
from blog import app, bcrypt, db, login_manager, SENDER, HOST, PASSWORD
from blog.forms import RegistrationForm, LoginForm, CreatePostForm, UpdateUserForm, ResetPasswordForm, ResetRequest
from blog.models import User, Post
from flask import flash, render_template, redirect, request, url_for, abort, current_app
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf.form import Form
from PIL import Image
from smtplib import SMTP


@login_manager.user_loader
def load_user(user_id):
	return db.get_or_404(User, user_id)


@app.route("/")
def home():
	page = request.args.get("page", 1, type=int)
	posts = db.paginate(db.select(Post).order_by(Post.date_posted.desc()), page=page, per_page=5)
	return render_template("home.html", pagetitle="HomePage", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegistrationForm()
	# Checks whether the user is logged in or not
	if current_user.is_authenticated:
		flash("You are already logged in", "info")
		return redirect(url_for("home"))
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
	# Checks whether the user is logged in or not
	if current_user.is_authenticated:
		flash("You are already logged in", "info")
		return redirect(url_for("home"))
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
			title=form.heading.data,
			description=form.description.data,
			post_image=form.post_image.data,
			content=form.content.data,
			author=current_user
		)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for("home"))
	return render_template("create_post.html", form=form, value="Create")


@app.route("/update_post/<int:post_id>", methods=["GET", "POST"])
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
		return redirect(url_for("show_post", post_id=post.id))
	form.heading.data = post.title
	form.description.data = post.description
	form.post_image.data = post.post_image
	form.content.data = post.content
	return render_template("create_post.html", form=form, post=post, value="Update")


@app.route("/delete_post/<int:post_id>")
@login_required
def delete_post(post_id):
	post = db.session.execute(db.select(Post).where(Post.id==post_id)).scalar()
	if current_user.id != post.author_id:
		abort(401)
	db.session.delete(post)
	db.session.commit()
	flash("Your post has been successfully deleted", "success")
	return redirect(url_for("home"))


@app.route("/show_post/<int:post_id>")
def show_post(post_id):
	post = db.session.execute(db.select(Post).where(Post.id==post_id)).scalar()
	if not post:
		flash("Invalid input provided.", "warning")
		return redirect(url_for("home"))
	return render_template("post.html", post=post, date=post.date_posted.strftime("%Y-%m-%d"))


def save_profile_pictures(profile_picture):
	"""This will take a arg (Format: filename.extension) as form data.
	It will create a thumbnail of size (150, 150)."""
	hex_name = secrets.token_hex(8)
	_, file_extn = os.path.splitext(profile_picture.filename)
	pic_filename = hex_name + file_extn
	pic_directory = os.path.join(current_app.root_path, "static/profile_pics", pic_filename)
	image_size = (150, 150)
	profile_pic = Image.open(profile_picture)
	profile_pic.thumbnail(image_size)
	profile_pic.save(pic_directory)
	return pic_filename


@app.route("/profile", methods=["GET", "POST"])
def profile():
	form = UpdateUserForm()
	# Checks whether the user is not logged in.
	if not current_user.is_authenticated:
		flash("You cannot access this page before logging in.", "warning")
		return redirect(url_for("login"))
	if form.validate_on_submit():
		if form.profile_image.data:
			new_profile_photo = save_profile_pictures(form.profile_image.data)
			current_user.profile_photo = new_profile_photo
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your profile has been updated", "success")
		return redirect(url_for("profile"))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.profile_photo)
	return render_template("profile.html", form=form, image_file=image_file)


def send_reset_mail(user):
	token = user.generate_reset_token()
	# TODO: Create a mailing function
	with SMTP(host=HOST, port=587) as connection:
		connection.starttls()
		connection.login(user=SENDER, password=PASSWORD)
		connection.sendmail(
			from_addr=SENDER,
			to_addrs=user.email,
			msg=f"""Subject: Reset password request\n\n 
Please click the following link to reset your password : {url_for("reset_password", token=token, _external=True)} 
If the reset was not initiated by you, do not proceed with the link and no changes will be made.
If this message was received to the wrong user, we apologies for the incovinence and confusion."""
)



@app.route("/reset_request", methods=["GET", "POST"])
def reset_request():
	# Checks whether the user is logged in or not
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = ResetRequest()
	print("before post")
	if form.validate_on_submit():
		print("after post")
		user = db.session.execute(db.select(User).where(User.email==form.email.data)).scalar_one_or_none()
		print(form.email.data, user.email)
		if user:
			send_reset_mail(user)
			flash("A mail has successfully been send to your email.", "success")
			return redirect(url_for("login"))
		else:
			flash("Invalid input. Provided email not registered.")
			return redirect(url_for("register"))
	return render_template("reset_request.html", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
	# Checks whether the user is logged in or not
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	user = User.verify_reset_token(token)
	if user is None:
		flash("This is a invalid or expired link", "warning")
		return redirect(url_for("login"))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data)
		user.password = hash_password
		db.session.commit()
		flash("Your password has successfully updated. Please try to login.", "success")
		return redirect(url_for("login"))
	return render_template("reset_password.html", form=form)


@app.route("/filter_post/<name>")
def filter_post(name):
	user_data = db.session.execute(db.select(User).where(User.username==name)).scalar()
	page = request.args.get("page", 1, type=int)
	get_single_users_posts = db.paginate(db.select(Post).filter_by(author_id=user_data.id).order_by(Post.date_posted.desc()), page=page, per_page=5)
	return render_template("home.html", posts=get_single_users_posts, filter=True, name=name)
