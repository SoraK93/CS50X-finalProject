from blog import db
from blog.models import User, Post
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    """Form used when user wants to register/ sign-up in our app"""
    username = StringField("Username", validators=[DataRequired(message="Provide username. Field cannot be empty."), Length(max=20, message="Max Length of 20.")])
    email = EmailField("Email", validators=[DataRequired(message="Provide Email. Field cannot be empty."), Email(message="Please enter a valid E-mail Address")])
    password = PasswordField("Password", validators=[DataRequired(message="Cannot be empty.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(message="Cannot be empty."), EqualTo("password", message="Must match password.")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar_one_or_none()
        if user:
            raise ValidationError(message="Username is already registered. Please try to sign in.")
        
    def validate_email(self, email):
        user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
        if user:
            raise ValidationError("Email is already registered. Please try to sign in.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Provide username. Field cannot be empty."), Length(max=20, message="Max Length of 20.")])
    password = PasswordField("Password", validators=[DataRequired(message="Cannot be empty.")])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

