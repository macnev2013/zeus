from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from zeus import db
from zeus.database.uptime import UptimeWebsiteDetails
from zeus.uptime import bp
from zeus.uptime.forms import UptimeAddSiteForm


@login_required
@bp.route('/', methods=['GET', 'POST'])
def uptime():
    add_site_form = UptimeAddSiteForm(request.form)
    action = request.form.get('action')
    if request.method == 'POST' and add_site_form.validate():
        if action == 'save':
            website = add_site_form.url.data
            uptime_websites = UptimeWebsiteDetails(username=current_user.username, website=website)
            db.session.add(uptime_websites)
            db.session.commit()
    website_list = UptimeWebsiteDetails.query.filter_by(username=current_user.username).all()
    return render_template('uptime/uptime.html', page='uptime', form=add_site_form)
