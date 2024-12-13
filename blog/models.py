from blog import db
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship


# This table is for storing Users information
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    profile_photo: Mapped[str] = mapped_column(String(20), nullable=False, default="default.jpg")
    # Below line will link user table to post table
    user_post = relationship("Post", back_populates="author")
    # Below line will link user table to comment table
    user_comment = relationship("Comment", back_populates="user")

    def generate_reset_token(self):
        """Creates a reset token, which will then be sent to the user through mail"""
        serialize = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="reset password")
        # Variable is used to call URLSafeTimedSerializer function, which will then create a url
        # which records its time of creation. We are using user's id to create this token
        return serialize.dumps({"user_id": self.id})
    
    @staticmethod
    def verify_reset_token(token, expire=1800):
        """Verifies the token by checking its time of creation, salt, secret key"""
        serialize = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="reset password")
        # Token received through the link should match this token here, else the result will be None.
        try:
            user_id = serialize.loads(token, salt="reset password", max_age=expire)["user_id"]
        except:
            return None
        
        return db.session.execute(db.select(User).where(User.id==user_id)).scalar()


# This table stores Posts created by Users.
# Post table has a many(post)-to-one(user) relationship with User table
# Post table has a many(comment)-to-one(post) relationship with Comment table
class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(120), nullable=False)
    post_image: Mapped[str] = mapped_column(String(300), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_posted: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    # Below lines will link post table to user table
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    author = relationship("User", back_populates="user_post")
    # Below lines will link post table to comment table
    post_comment = relationship("Comment", back_populates="feedback")


# This table stores Users comment made on any individual post
class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # These lines will link user to comment table in a one-to-many relationship
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="user_comment")
    # These lines will link post to comment table in a one-to-many relationship
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)
    feedback = relationship("Post", back_populates="post_comment")

