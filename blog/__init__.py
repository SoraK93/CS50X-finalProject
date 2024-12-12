import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Loads .env file
load_dotenv()


# Database Initialize
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Flask app Initialize
app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
db.__init__(app)

# Login Manager Initialize
login_manager = LoginManager()
login_manager.__init__(app)

# Bcrypt Initialize
bcrypt = Bcrypt(app)

# Ckeditor Initialize
ckeditor = CKEditor(app)

# Email setup
HOST = os.environ["EMAIL_SMTP"]
SENDER = os.environ["EMAIL_USER"]
PASSWORD = os.environ["EMAIL_PASS"]

from blog import routes

with app.app_context():
    db.create_all()
