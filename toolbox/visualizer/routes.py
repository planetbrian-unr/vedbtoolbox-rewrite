# flask and its plugins
from flask import render_template

# local
from toolbox.visualizer import blueprint

@blueprint.route("/visualizer")
def visualizer():
    return render_template("visualizer/visualizer.html")
