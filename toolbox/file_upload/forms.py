# written by brian
# defined basic URL input fields as to avoid literally creating a HTML form
# avoids directly checking POST requests in routes.py.

# flask (plugins)
from flask_wtf import FlaskForm

# pip. used for above
from wtforms import URLField, SubmitField
from wtforms.validators import URL

# classes defining forms that appear on page
class DatabraryURLForm(FlaskForm):
    url = URLField("Databrary Session URL", validators=[URL()])
    submit = SubmitField()

class OSFURLForm(FlaskForm):
    url = URLField("OSF Session URL", validators=[URL()])
    submit = SubmitField()
