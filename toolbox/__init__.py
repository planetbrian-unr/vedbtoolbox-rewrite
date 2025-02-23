# base
import os

# pip packages
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from authlib.integrations.flask_client import OAuth

# local stuff
from .models import db, User

def create_app():
    # configure Flask app with variables from config.py. refer to resources/codebase-structure.txt
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("toolbox.config.Config")
    
    # read .env file for auth0 variables
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)
    
    # configure authlib to handle application authentication with auth0
    oauth = OAuth(app)
    oauth.register(
        "auth0",
        client_id=os.environ.get("AUTH0_CLIENT_ID"),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={"scope": "openid profile email",},
        server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )
    
    # set up database to locally store Auth0 stuff for our use
    db.init_app(app)
    
    # Use a context manager to ensure the app context is available for db operations
    with app.app_context():
        # import routes
        from toolbox import auth
        
        app.add_url_rule("/", "home", auth.home)
        app.add_url_rule("/login", "login", auth.login)
        app.add_url_rule("/callback", "callback", auth.callback, methods=["GET", "POST"])
        app.add_url_rule("/logout", "logout", auth.logout)
        
        db.create_all()
    
    return app
