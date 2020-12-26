from wtforms import Form, StringField, PasswordField, validators


class GitForm(Form):
    git_username = StringField('Username',
                               validators=[validators.DataRequired()],
                               render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Git Username'})

    git_password = PasswordField('Password',
                                 validators=[validators.DataRequired()],
                                 render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Git Password'})


class AWSForm(Form):
    aws_access_key = StringField('AWS Access Key',
                                 render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'AWS Access Key'})

    aws_secret_key = PasswordField('AWS Secret Key',
                                   render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'AWS Secret Key'})
