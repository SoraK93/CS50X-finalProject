from blog import bcrypt, db
from blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm, ResetPasswordForm, ResetRequest
from blog.models import User
from flask import flash, render_template, redirect, request, url_for, Blueprint
from flask_login import login_user, logout_user, current_user
from blog.users.utilities import save_profile_pictures, send_reset_mail

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
	form = RegistrationForm()
	# Checks whether the user is logged in or not
	if current_user.is_authenticated:
		flash("You are already logged in", "info")
		return redirect(url_for("main.home"))
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
		return redirect(url_for("users.login"))
	return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	# Checks whether the user is logged in or not
	if current_user.is_authenticated:
		flash("You are already logged in", "info")
		return redirect(url_for("main.home"))
	if form.validate_on_submit():
		email = form.email.data
		user = db.session.execute(db.select(User).where(User.email==email)).scalar()
		if user:
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				return redirect(url_for("main.home"))
			else:
				flash("Incorrect Email/ Password provided. Please check user credentials.", "danger")
				return redirect(url_for("users.login"))	
		else:
			flash("User not registered. Please register here.", "warning")
			return redirect(url_for("users.register"))
	return render_template("login.html", form=form)


@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("main.home"))


@users.route("/profile", methods=["GET", "POST"])
def profile():
	form = UpdateUserForm()
	# Checks whether the user is not logged in.
	if not current_user.is_authenticated:
		flash("You cannot access this page before logging in.", "warning")
		return redirect(url_for("users.login"))
	if form.validate_on_submit():
		if form.profile_image.data:
			new_profile_photo = save_profile_pictures(form.profile_image.data)
			current_user.profile_photo = new_profile_photo
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your profile has been updated", "success")
		return redirect(url_for("users.profile"))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.profile_photo)
	return render_template("profile.html", form=form, image_file=image_file)


@users.route("/reset_request", methods=["GET", "POST"])
def reset_request():
	# Checks whether the user is logged in or not
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form = ResetRequest()
	if form.validate_on_submit():
		user = db.session.execute(db.select(User).where(User.email==form.email.data)).scalar_one_or_none()
		if user:
			send_reset_mail(user)
			flash("A mail has successfully been send to your email.", "success")
			return redirect(url_for("users.login"))
		else:
			flash("Invalid input. Provided email not registered.")
			return redirect(url_for("users.register"))
	return render_template("reset_request.html", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
	# Checks whether the user is logged in or not
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	user = User.verify_reset_token(token)
	if user is None:
		flash("This is a invalid or expired link", "warning")
		return redirect(url_for("users.login"))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data)
		user.password = hash_password
		db.session.commit()
		flash("Your password has successfully updated. Please try to login.", "success")
		return redirect(url_for("users.login"))
	return render_template("reset_password.html", form=form)
