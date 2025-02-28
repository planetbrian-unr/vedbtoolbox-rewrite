# flask and its plugins
from flask import render_template

# local
from toolbox.file_upload import blueprint
from toolbox.file_upload.forms import DatabraryURLForm, OSFURLForm

@blueprint.route("/file_upload")
def file_upload():
    databrary_url_form = DatabraryURLForm()
    osf_url_form = OSFURLForm()
    return render_template("file_upload/file_upload.html", databrary_url_form=databrary_url_form, osf_url_form=osf_url_form)
