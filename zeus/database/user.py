import jwt
from flask import current_app
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from zeus import db, login
import logging

LOGGER = logging.getLogger(__name__)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    git_username = db.Column(db.String(128))
    git_password = db.Column(db.String(128))

    aws_access_key = db.Column(db.String(128))
    aws_secret_key = db.Column(db.String(128))

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_git_config(self, git_username, git_password):
        self.git_username = git_username
        self.git_password = git_password

    def get_git_config(self):
        return self.git_username, self.git_password

    def delete_git_config(self):
        self.git_username = None
        self.git_password = None

    def set_aws_config(self, aws_access_key, aws_secret_key):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

    def get_aws_config(self):
        return self.aws_access_key, self.aws_secret_key

    def delete_aws_config(self):
        self.aws_access_key = None
        self.aws_secret_key = None

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
