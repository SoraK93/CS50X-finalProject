import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ["FLASK_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    # Email setup
    HOST = os.environ["EMAIL_SMTP"]
    SENDER = os.environ["EMAIL_USER"]
    PASSWORD = os.environ["EMAIL_PASS"]
    