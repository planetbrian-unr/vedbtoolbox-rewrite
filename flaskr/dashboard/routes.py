# flask and its plugins
from flask import render_template, redirect
from flask_login import current_user

# local
from flaskr.models import User
from flaskr.dashboard import blueprint

@blueprint.route("/dashboard")
def dashboard():
    if not User.query.filter_by(username=current_user.username).first().admin:
        return redirect("/file_upload")
    return render_template("dashboard/dashboard.html")
