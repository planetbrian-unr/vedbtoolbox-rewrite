import secrets
from os import environ

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from authlib.integrations.flask_client import OAuth

# read .env file
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# configure Flask app
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe()

# configure authlib to handle application authentication with auth0
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=environ.get("AUTH0_CLIENT_ID"),
    client_secret=environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# import routes
from . import auth



