# flask and its plugins
from flask import render_template

# local
from toolbox.dashboard import blueprint

@blueprint.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")
