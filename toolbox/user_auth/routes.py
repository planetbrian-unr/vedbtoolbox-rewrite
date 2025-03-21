# base
from os import environ as env

# pip packages
from urllib.parse import quote_plus, urlencode

# flask stuff
from flask import url_for, session, redirect

# local
from toolbox.user_auth import blueprint
from toolbox.user_auth.oauth import oauth
from toolbox.user_auth.methods import add_user_to_local_db

@blueprint.route("/login")
def login():
	return oauth.auth0.authorize_redirect(
		redirect_uri = url_for("user_auth.callback", _external=True)
	)

# finalizing authentication
@blueprint.route("/callback")
def callback():
	token = oauth.auth0.authorize_access_token()
	session["user"] = token
	
	# take token's components and add the relevant fields to the local user db
	add_user_to_local_db(token)
	
	# redirect to file upload page, like the original application
	return redirect("/")


# clearing session
@blueprint.route("/logout")
def logout():
	session.clear()
	
	return redirect(
		"https://" + env.get("AUTH0_DOMAIN") + "/v2/logout?" + 
		urlencode(
			{
				"returnTo": url_for("home.home", _external=True),
				"client_id": env.get("AUTH0_CLIENT_ID"),
			},
			quote_via = quote_plus,
		)
	)
