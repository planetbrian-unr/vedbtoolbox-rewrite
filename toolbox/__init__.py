# guide: https://hackersandslackers.com/flask-application-factory/
# guide: https://github.com/app-generator/flask-datta-able

# base
from importlib import import_module

# flask and its plugins
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_dropzone import Dropzone
from flask_minify import Minify # mini-fies all files for better deployment
from flask_wtf.csrf import CSRFProtect


# globally accessible objects
db = SQLAlchemy()
bootstrap = Bootstrap5()
csrf = CSRFProtect()
dropzone = Dropzone()

def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    dropzone.init_app(app)

def register_blueprints(app, bp_list):
    for module_name in bp_list:
        module = import_module('toolbox.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_app(test_config=None):
    # initialize core application
    app = Flask(__name__, instance_relative_config=True)

    if test_config == None:
        app.config.from_object("toolbox.config.Config")
    if test_config == True:
        app.config.from_object("toolbox.config.TestingConfig")

    Minify(app, html=True, js=True, cssless=True)

    register_extensions(app)

    # blueprints
    blueprint_list = ["home", "user_auth", "file_upload", "visualizer", "dashboard"]
    register_blueprints(app, blueprint_list)

    with app.app_context():
        db.create_all()
        
    return app
