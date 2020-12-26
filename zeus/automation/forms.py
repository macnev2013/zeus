from wtforms import Form, StringField, BooleanField, validators


class NodeJSForm(Form):
    git_url = StringField(
        'Git URL',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Git URL'}
    )

    production_branch = StringField(
        'Production Branch',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Production Branch'}
    )

    development_branch = StringField(
        'Development Branch',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Development Branch'}
    )

    project_name = StringField(
        'Project Name',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Project Name'}
    )

    service_name = StringField(
        'Service Name',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Service Name'}
    )

    system_port = StringField(
        'System Port',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'System Port'}
    )

    cont_port = StringField(
        'Container Port',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Container Port'}
    )

    sshagent_name = StringField(
        'SSH Agent Name (Prod)',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'SSH Agent Name (Prod)'}
    )

    ip_address = StringField(
        'IP Address (Prod)',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'IP Address (Prod)'}
    )

    checkbox = BooleanField(
        'Do you want to integrate Jenkins ?',
        id='jenkins-users-cb',
        render_kw={'class': 'form-check-input mr-3', 'placeholder': 'Do you want to integrate Jenkins ?'}
    )

    jenkins_users = StringField(
        'Jenkins User Access',
        id='jenkins-users-input',
        validators=[validators.DataRequired()],
        render_kw={'class': 'd-none form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Jenkins User Access'}
    )


class JavaForm(Form):
    var_git_url = StringField(
        'Git URL',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Git URL'}
    )

    var_git_branch_prod = StringField(
        'Production Branch',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Production Branch'}
    )

    var_git_branch_dev = StringField(
        'Development Branch',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Development Branch'}
    )

    var_project_name = StringField(
        'Project Name',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Project Name'}
    )

    var_service_name = StringField(
        'Service Name',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Service Name'}
    )

    var_system_port = StringField(
        'System Port',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'System Port'}
    )

    var_cont_port = StringField(
        'Container Port',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Container Port'}
    )

    var_ssh_agent_name = StringField(
        'SSH Agent Name (Prod)',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'SSH Agent Name (Prod)'}
    )

    var_ip_addr = StringField(
        'IP Address (Prod)',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'IP Address (Prod)'}
    )

    var_jar_name = StringField(
        'JAR Name',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'JAR Name'}
    )

    var_max_memory = StringField(
        'Max Memory',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Max Memory'}
    )

    checkbox = BooleanField(
        'Do you want to integrate Jenkins ?',
        render_kw={'class': 'form-check-input mr-3', 'placeholder': 'Do you want to integrate Jenkins ?'}
    )

    var_jenkins_users = StringField(
        'Jenkins User',
        validators=[validators.DataRequired()],
        render_kw={'class': 'd-none form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Jenkins User Access'}
    )
