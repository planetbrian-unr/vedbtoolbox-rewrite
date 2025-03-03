# flask and its plugins
from flask import render_template

# local
from toolbox.home import blueprint

@blueprint.route("/")
def home():
    return render_template("home/home.html")

@blueprint.route("/team")
def team():
    return render_template("home/team.html")

@blueprint.route("/faculty")
def faculty():
    return render_template("home/faculty.html")

@blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template("home/404.html"), 404
