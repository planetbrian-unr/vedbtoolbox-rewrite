# written by brian
# defined basic URL input fields as to avoid literally creating a HTML form
# avoids directly checking POST requests in routes.py.
# defined WTForm classes for URL input as to:
#   avoid literally creating an HTML form on the page and generating a POST request
#    - in the original write, this was the case. rather unwieldy!

# flask (plugins)
from flask_wtf import FlaskForm

# pip. used for above
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, URL

# classes defining forms that appear on page
class DatabraryURLForm(FlaskForm):
	url = URLField("Databrary URL", validators=[DataRequired(), URL()])
	submit = SubmitField("Submit URL")

class OSFURLForm(FlaskForm):
	url = URLField("OSF URL", validators=[DataRequired(), URL()])
	submit = SubmitField("Submit URL")
	
class EnterVisualizer(FlaskForm):
	submit = SubmitField("Enter Visualizer")
