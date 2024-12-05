from blog import app, bcrypt, db, login_manager
from blog.models import User, Post
from flask import flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user
from flask_wtf.form import Form
from blog.forms import RegistrationForm, LoginForm


@login_manager.user_loader
def load_user(user_id):
	return db.get_or_404(User, user_id)


@app.route("/")
def home():
	return render_template("home.html", pagetitle="HomePage")


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
		flash(message="You have registered successfully.", category="success")
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


@app.route("/post")
@login_required
def post():
	return render_template("post.html")