# base
import os

# pip packages
from urllib.parse import quote_plus, urlencode

# flask stuff
from flask import url_for, session, redirect

# local
from toolbox import db
from toolbox.models import User
from toolbox.auth import blueprint
from toolbox.auth.oauth import oauth

@blueprint.route("/login")
def login():
	return oauth.auth0.authorize_redirect(
		redirect_uri=url_for("auth_bp.callback", _external=True)
	)


# finalizing authentication
@blueprint.route("/callback")
def callback():
	token = oauth.auth0.authorize_access_token()
	session["user"] = token
	

	# parse returned json in token and add attributes to our local db
	# Parse the user info from the token's userinfo field
	user_info = token.get("userinfo", {})
	json_user_id = user_info.get("sub")
	json_username = user_info.get("nickname", "")
	json_email = user_info.get("email")
	
	# Add or update the user in the database
	user_in_db = User.query.filter_by(id=json_user_id).first()
	if not user_in_db:
		# Add new user if not already in the database
		user_in_db = User(
			id=json_user_id,
			username=json_username,
			email=json_email,
		)
		db.session.add(user_in_db)
	else:
		# Update existing user if necessary
		user_in_db.username = json_username
		user_in_db.email = json_email
	
	db.session.commit()
	
	return redirect("/")


# clearing session
@blueprint.route("/logout")
def logout():
	session.clear()
	return redirect(
		"https://" + os.environ.get("AUTH0_DOMAIN")
		+ "/v2/logout?"
		+ urlencode(
			{
				"returnTo": url_for("home", _external=True),
				"client_id": os.environ.get("AUTH0_CLIENT_ID"),
			},
			quote_via=quote_plus,
		)
	)
