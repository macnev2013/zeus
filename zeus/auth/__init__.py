from flask import Blueprint

bp = Blueprint('auth', __name__)

from zeus.auth import routes