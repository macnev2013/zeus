from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from zeus import db
from zeus.database.user import User
from zeus.uptime import bp
from zeus.uptime.forms import UptimeAddSiteForm


@login_required
@bp.route('/', methods=['GET', 'POST'])
def uptime():
    form = UptimeAddSiteForm(request.form)
    return render_template('uptime/uptime.html', page='uptime', form=form)
