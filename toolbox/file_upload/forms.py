# written by brian
# defined WTForm classes for URL input as to:
#   avoid literally creating an HTML form on the page and generating a POST request
#    - in the original write, this was the case. rather unwieldy!

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
