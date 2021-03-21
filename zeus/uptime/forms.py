from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import EqualTo

class UptimeAddSiteForm(Form):
    url = StringField(
        'URL',
        validators=[validators.DataRequired()],
        render_kw={'class': 'form-control border-0 shadow-none custom-input my-3', 'placeholder': 'URL'}
    )