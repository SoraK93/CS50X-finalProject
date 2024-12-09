from blog import db
from blog.models import User, Post
from flask_ckeditor import CKEditorField
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL


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
    """Form used for user login purposes"""
    email = EmailField("Email", validators=[DataRequired(message="Provide Email for Login."), Email(message="Please enter a valid E-mail Address")])
    password = PasswordField("Password", validators=[DataRequired(message="Cannot be empty.")])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class CreatePostForm(FlaskForm):
    """When registered user wants to post about something, this form is used"""
    heading = StringField("Heading", validators=[DataRequired("Cannot have empty heading."), Length(max=50, message="Cannot be more than 50 words.")])
    description = StringField("Description", validators=[DataRequired("Cannot post without providing description."), Length(max=240, message="Cannot be more than 240 words")])
    post_image = StringField("Post Image URL", validators=[DataRequired("Cannot post without a URL."), URL()])
    content = CKEditorField("Content", validators=[DataRequired("Cannot post with empty content."), Length(min=1, message="Cannot create a empty post.")])
    submit = SubmitField("Create Post")


class UpdateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Provide username. Field cannot be empty."), Length(max=20, message="Max Length of 20.")])
    email = EmailField("Email", validators=[DataRequired(message="Provide Email. Field cannot be empty."), Email(message="Please enter a valid E-mail Address")])
    profile_image = FileField("Upload Profile Image", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update profile")

    def validate_username(self, username):
        if current_user.username != username.data:
            user = db.session.execute(db.select(User).where(User.username==username.data)).scalar_one_or_none()
            if user:
                raise ValidationError("Username is already taken. Please try a different name.")
            
    def validate_email(self, email):
        if current_user.email != email.data:
            user = db.session.execute(db.select(User).where(User.username==email.data)).scalar_one_or_none()
            if user:
                raise ValidationError("Email is already taken. Please try a different name.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(message="Cannot be empty.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(message="Cannot be empty."), EqualTo("password", message="Must match password.")])
    submit = SubmitField("Confirm Password")