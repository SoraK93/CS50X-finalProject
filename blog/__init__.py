from blog.config import Config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Database Initialize
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

bcrypt = Bcrypt()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    # Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Bcrypt Initialize
    bcrypt.__init__(app)
    ckeditor.__init__(app)
    db.__init__(app)
    login_manager.__init__(app)
    
    from blog.main.routes import main
    from blog.users.routes import users
    from blog.posts.routes import posts
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    with app.app_context():
        db.create_all()

    return app