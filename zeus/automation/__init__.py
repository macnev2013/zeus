from flask import Blueprint

bp = Blueprint('automation', __name__)

from zeus.automation import routes