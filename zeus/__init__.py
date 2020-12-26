import logging
from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from zeus.automation import bp as automation_bp
    app.register_blueprint(automation_bp, url_prefix='/automation')

    from zeus.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from zeus.settings import bp as settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')

    return app

from zeus.database import user
