from flask_wtf import FlaskForm
from wtforms import URLField, ValidationError
from wtforms.validators import URL
from urllib.parse import urlparse

def domain_match_validator(expected_domain):
    def _domain_match(field):
        if urlparse(field.data).netloc != expected_domain:
            raise ValidationError(f"URL must be from the domain {expected_domain}.")
    return _domain_match

class DatabraryURLForm(FlaskForm):
    url = URLField("Databrary Session URL", validators=[URL(), domain_match_validator("databrary.org")])

class OSFURLForm(FlaskForm):
    url = URLField("OSF Session URL", validators=[URL(), domain_match_validator("osf.io")])