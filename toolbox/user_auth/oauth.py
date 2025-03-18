# base
from os import environ as env

# pip packages
from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth

# flask
from flask import current_app

# read .env file for auth0 variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

oauth = OAuth(current_app)

oauth.register(
    "auth0",
    client_id = env.get("AUTH0_CLIENT_ID"),
    client_secret = env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs = {
        "scope": "openid profile email"
    },
    server_metadata_url = f"https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration"
)