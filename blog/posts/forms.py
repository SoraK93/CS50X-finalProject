from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL


class CreatePostForm(FlaskForm):
    """When registered user wants to post about something, this form is used"""
    heading = StringField("Heading", validators=[DataRequired("Cannot have empty heading."), Length(max=50, message="Cannot be more than 50 words.")])
    description = StringField("Description", validators=[DataRequired("Cannot post without providing description."), Length(max=240, message="Cannot be more than 240 words")])
    post_image = StringField("Post Image URL", validators=[DataRequired("Cannot post without a URL."), URL()])
    content = CKEditorField("Content", validators=[DataRequired("Cannot post with empty content."), Length(min=1, message="Cannot create a empty post.")])
    submit = SubmitField("Create Post")


class CommentForm(FlaskForm):
    comment = CKEditorField("Content", validators=[DataRequired("Cannot post with empty content."), Length(min=1, message="Cannot create a empty post.")])
    submit_comment = SubmitField("Create Post")