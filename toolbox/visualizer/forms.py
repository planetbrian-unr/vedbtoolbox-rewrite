from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import URLField, StringField
from wtforms.validators import DataRequired

class VideoUpload(FlaskForm):
    videos = FileField("videofiles", validators=[FileRequired()])