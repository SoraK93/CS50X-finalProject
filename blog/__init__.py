import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Initial Config
load_dotenv()
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
bcrypt = Bcrypt(app)
db.__init__(app)
login_manager = LoginManager()
login_manager.__init__(app)

from blog import routes
