# flask and its plugins
from flask import render_template

# local
from toolbox.visualizer import blueprint
from toolbox.visualizer.forms import VideoFiles

@blueprint.route("/visualizer")
def visualizer():
    form = VideoFiles()
    return render_template("visualizer_bp/file_upload.html", form=form)