from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
import re
from zeus import db, scheduler, LIST_OF_WEBSITE_TO_CHECK
from zeus.database.uptime import UptimeWebsiteDetails
from zeus.uptime import bp
from zeus.uptime.forms import UptimeAddSiteForm
import requests

REGEX = '^((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9_-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?$'

@login_required
@bp.route('/', methods=['GET', 'POST'])
def uptime():
    add_site_form = UptimeAddSiteForm(request.form)
    if request.method == 'POST' and add_site_form.validate():
        if request.form.get('action') == 'save':
            website = add_site_form.url.data
            if not re.match(REGEX, website):
                return redirect(url_for('uptime.uptime'))
            UptimeWebsiteDetails.add_website(username=current_user.username, website=website)
            add_site_to_schedular(website=website)
            add_site_form.url.data = ''
    websites = UptimeWebsiteDetails.get_websites_for_user(username=current_user.username)
    return render_template('uptime/uptime.html', page='uptime', form=add_site_form, websites=websites)


@login_required
@bp.route('/remove', methods=['GET', 'POST'])
def remove():
    UptimeWebsiteDetails.delete_website(request.args.get('id'))
    return redirect(url_for('uptime.uptime'))


def add_site_to_schedular(website):
    LIST_OF_WEBSITE_TO_CHECK.append({'website': website, 'status': 'up'})
    print(LIST_OF_WEBSITE_TO_CHECK)


@scheduler.task('interval', id='fetch_status', seconds=10, misfire_grace_time=10)
def fetch_status():
    print('started')
    for website in LIST_OF_WEBSITE_TO_CHECK:
        status = requests.head(website).status_code
        if status != 200:
            print('E')
    print('Done')