# flask + pip
from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import URL

# classes defining forms that appear on page
class DatabraryURLForm(FlaskForm):
    url = URLField("Databrary Session URL", validators=[URL()])
    submit = SubmitField()

class OSFURLForm(FlaskForm):
    url = URLField("OSF Session URL", validators=[URL()])
    submit = SubmitField()
