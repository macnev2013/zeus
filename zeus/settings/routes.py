import logging

from flask import request, render_template
from flask_login import login_required, current_user

from zeus import db
from zeus.settings import bp
from zeus.settings.forms import GitForm, AWSForm

LOGGER = logging.getLogger(__name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def settings():
    git_form = GitForm(request.form)
    aws_form = AWSForm(request.form)
    action = request.form.get('action')

    LOGGER.error('Cool %s' % (current_user.__dict__))
    if request.method == 'POST' and git_form.validate():
        git_username = git_form.data.get('git_username')
        git_password = git_form.data.get('git_password')

        aws_access_key = aws_form.data.get('aws_access_key')
        aws_secret_key = aws_form.data.get('aws_secret_key')

        if action == 'save':
            current_user.set_git_config(git_username, git_password)
            db.session.commit()
        if action == 'delete':
            if git_username == current_user.git_username:
                current_user.delete_git_config()
                db.session.commit()

    if request.method == 'POST' and aws_form.validate():
        if action == 'save':
            current_user.set_aws_config(aws_access_key, aws_secret_key)
            db.session.commit()
        if action == 'delete':
            if git_username == current_user.aws_access_key:
                current_user.delete_aws_config()
                db.session.commit()

    if current_user.git_username:
        git_form.git_username.data = current_user.git_username
    else:
        git_form.git_username.data = ''

    if current_user.aws_access_key:
        git_form.aws_access_key.data = current_user.aws_access_key
    else:
        git_form.aws_access_key.data = ''

    return render_template('settings/settings.html',
                           page='settings',
                           git_form=git_form, aws_form=aws_form)
