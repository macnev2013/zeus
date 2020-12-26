from flask import request, render_template
from flask_login import login_required

from zeus.automation import bp
from zeus.automation.forms import NodeJSForm, JavaForm


@bp.route('/', methods=['GET'])
@login_required
def automation():
    return render_template('automation/automation.html', page='automation')


@bp.route('/nodejs', methods=['GET'])
@login_required
def nodejs():
    nodejs_form = NodeJSForm(request.form)
    # if request.method == 'POST' and nodejs_form.validate():
    #     git_url = nodejs_form.data.get('git_url')
    #     production_branch = nodejs_form.data.get('production_branch')
    #     development_branch = nodejs_form.data.get('development_branch')
    #     project_name = nodejs_form.data.get('project_name')
    #     service_name = nodejs_form.data.get('service_name')
    #     system_port = nodejs_form.data.get('system_port')
    #     cont_port = nodejs_form.data.get('cont_port')
    #     sshagent_name = nodejs_form.data.get('sshagent_name')
    #     ip_address = nodejs_form.data.get('ip_address')
    #     checkbox = nodejs_form.data.get('checkbox')
    #     jenkins_users = nodejs_form.data.get('jenkins_users')
    return render_template('automation/nodejs.html', page='automation', nodejs_form=nodejs_form)


@bp.route('/java', methods=['GET'])
@login_required
def java():
    java_form = JavaForm(request.form)
    return render_template('automation/java.html', page='automation', java_form=java_form)
