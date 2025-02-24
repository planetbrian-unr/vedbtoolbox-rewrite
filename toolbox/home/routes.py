# flask and its plugins
from flask import render_template

# local
from toolbox.home import blueprint

@blueprint.route("/")
def home():
    return render_template("home_bp/home.html")

@blueprint.route("/team")
def team():
    return render_template("home_bp/team.html")

@blueprint.route("/faculty")
def faculty():
    return render_template("home_bp/faculty.html")