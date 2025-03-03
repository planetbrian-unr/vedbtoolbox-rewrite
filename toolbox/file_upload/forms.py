# flask + pip
from flask_wtf import FlaskForm
from wtforms import URLField, ValidationError, SubmitField
from wtforms.validators import URL
from urllib.parse import urlparse

# tests if entered URL matches provided argument
def domain_match_validator(expected_domain):
    def _domain_match(field):
        if expected_domain not in urlparse(field.data).netloc:
            raise ValidationError(f"URL must be from the domain {expected_domain}.")
    return _domain_match

# classes defining forms that appear on page
class DatabraryURLForm(FlaskForm):
    url = URLField("Databrary Session URL", validators=[URL(), domain_match_validator("nyu.databrary.org")])
    submit = SubmitField()

class OSFURLForm(FlaskForm):
    url = URLField("OSF Session URL", validators=[URL(), domain_match_validator("osf.io")])
    submit = SubmitField()
