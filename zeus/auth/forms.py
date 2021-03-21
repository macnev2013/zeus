from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import EqualTo


class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[validators.Length(min=4, max=25)],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Enter email or username'}
    )

    password = PasswordField(
        'Password',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Password'}
    )


class RegistrationForm(Form):
    username = StringField(
        'Username',
        validators=[validators.Length(min=4, max=25)],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Username'}
    )

    email = StringField(
        'Email',
        validators=[validators.Length(min=4, max=25)],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Email'}
    )

    password = PasswordField(
        'Password',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Password'}
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[validators.DataRequired(), EqualTo('password')],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'Confirm Password'}
    )
