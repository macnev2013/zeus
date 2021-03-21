from flask import Blueprint

bp = Blueprint('uptime', __name__)

from zeus.uptime import routes