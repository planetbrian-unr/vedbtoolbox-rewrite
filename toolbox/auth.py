import json
from os import environ

from flask import url_for, session, redirect, render_template
from urllib.parse import quote_plus, urlencode

from . import app, oauth

# home, will render an authenticated user's details, or allow sign-in
@app.route("/")
def home():
    return render_template("home.html", session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))

# trigger authentication
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

# finalizing authentication
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("/"))

# clearing session
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + environ.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
