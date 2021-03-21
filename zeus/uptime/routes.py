from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
import re
from zeus import db
from zeus.database.uptime import UptimeWebsiteDetails
from zeus.uptime import bp
from zeus.uptime.forms import UptimeAddSiteForm

REGEX = '^((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9_-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?$'

@login_required
@bp.route('/', methods=['GET', 'POST'])
def uptime():
    print('Calling this ')
    add_site_form = UptimeAddSiteForm(request.form)
    if request.method == 'POST' and add_site_form.validate():
        if request.form.get('action') == 'save':
            website = add_site_form.url.data
            if not re.match(REGEX, website):
                return redirect(url_for('uptime.uptime'))
            uptime_websites = UptimeWebsiteDetails(username=current_user.username, website=website)
            db.session.add(uptime_websites)
            db.session.commit()
            add_site_form.url.data = ''
    website_list = UptimeWebsiteDetails.query.with_entities(UptimeWebsiteDetails.id, UptimeWebsiteDetails.website).filter_by(username=current_user.username).all()
    return render_template('uptime/uptime.html', page='uptime', form=add_site_form, website_list=website_list)


@login_required
@bp.route('/remove', methods=['GET', 'POST'])
def remove():
    uptime_websites = UptimeWebsiteDetails.query.filter_by(id=request.args.get('id'))
    print('--------------------uptime_websites', uptime_websites)
    db.session.delete(uptime_websites)
    db.session.commit()
    return redirect(url_for('uptime.uptime'))