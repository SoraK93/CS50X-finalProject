from blog import app, bcrypt, db
from blog.models import User, Post
from flask import render_template, redirect, url_for, flash
from flask_wtf.form import Form
from blog.forms import RegistrationForm


@app.route("/")
def home():
	return render_template("home.html", pagetitle="HomePage")


@app.route("/login")
def login():
	return render_template("login.html")


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


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/contact")
def contact():
	return render_template("contact.html")


@app.route("/post")
def post():
	return render_template("post.html")