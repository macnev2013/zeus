from flask import Blueprint

bp = Blueprint('settings', __name__)

from zeus.settings import routes
