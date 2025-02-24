# guide: https://hackersandslackers.com/flask-application-factory/
# guide: https://github.com/app-generator/flask-datta-able

# base
from importlib import import_module

# flask and its plugins
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# globally accessible objects
db = SQLAlchemy()

def register_extensions(app):
    db.init_app(app)

def register_blueprints(app, list):
    for module_name in list:
        module = import_module('toolbox.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_app():
    # initialize core application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("toolbox.config.Config")

    register_extensions(app)

    # blueprints
    blueprint_list = ["home", "auth"]
    register_blueprints(app, blueprint_list)

    with app.app_context():
        db.create_all()
        
    return app
    