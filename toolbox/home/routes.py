# flask and its plugins
from flask import render_template

# local
from toolbox.home import blueprint

@blueprint.route("/")
def home():
    return render_template("home_bp/home.html")

@blueprint.route("/team_info")
def team_info():
    return render_template("home_bp/team.html")

@blueprint.route("/faculty_info")
def instructor_info():
    return render_template("home_bp/faculty.html")