# flask and its plugins
from flask import render_template

# local
from toolbox.file_upload import blueprint
from toolbox.file_upload.forms import DatabraryURLForm, OSFURLForm

@blueprint.route("/file_upload")
def file_upload():
    databrary_url = DatabraryURLForm()
    osf_url = OSFURLForm()
    return render_template("file_upload_bp/file_upload.html")