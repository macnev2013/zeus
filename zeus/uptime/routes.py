from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
import re
from zeus import db, scheduler, LIST_OF_UPTIME_WEBSITE_TO_CHECK
from zeus.database.uptime import UptimeWebsiteDetails
from zeus.uptime import bp
from zeus.uptime.forms import UptimeAddSiteForm
from zeus.uptime import controller
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
            add_site_form.url.data = ''
            try:
                if not any([website in item['website'] for item in LIST_OF_UPTIME_WEBSITE_TO_CHECK[current_user.username]]):
                    LIST_OF_UPTIME_WEBSITE_TO_CHECK[current_user.username].append({"website": website, "status": "down"})
            except ValueError:
                LIST_OF_UPTIME_WEBSITE_TO_CHECK[current_user.username] = []
                LIST_OF_UPTIME_WEBSITE_TO_CHECK[current_user.username].append({"website": website, "status": "down"})
            print("Added to the list", LIST_OF_UPTIME_WEBSITE_TO_CHECK)
    if current_user.username in LIST_OF_UPTIME_WEBSITE_TO_CHECK:
        websites = LIST_OF_UPTIME_WEBSITE_TO_CHECK[current_user.username]
    else:
        websites = UptimeWebsiteDetails.get_websites_for_user(username=current_user.username)
    return render_template('uptime/uptime.html', page='uptime', form=add_site_form, websites=websites)


@login_required
@bp.route('/remove', methods=['GET', 'POST'])
def remove():
    website = request.args.get('website')
    UptimeWebsiteDetails.delete_website(current_user.username, request.args.get('website'))
    for item in LIST_OF_UPTIME_WEBSITE_TO_CHECK[current_user.username]:
        if website in item['website']:
            print("Removed", website, "for user", current_user.username)
            LIST_OF_UPTIME_WEBSITE_TO_CHECK[current_user.username].remove({"website": item['website'], "status": item['status']})
    return redirect(url_for('uptime.uptime'))


@login_required
@bp.route('/status', methods=['GET'])
def status():
    return render_template('uptime/status.html', data=LIST_OF_UPTIME_WEBSITE_TO_CHECK)

# def add_site_to_schedular(website):
#     LIST_OF_UPTIME_WEBSITE_TO_CHECK.append({'website': website, 'status': 'up'})
    # print(LIST_OF_UPTIME_WEBSITE_TO_CHECK)