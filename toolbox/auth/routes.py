# base
from os import environ as env

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
		redirect_uri = url_for("auth.callback", _external=True)
	)

def add_user_to_local_db(token):
	# parse returned json in token for specific attributes
	user_info = token.get("userinfo", {})
	json_user_id = user_info.get("sub")
	json_username = user_info.get("nickname")
	json_email = user_info.get("email")
	
	# add/update the user in the database
	user_in_db = User.query.filter_by(user_id=json_user_id).first()
	if not user_in_db:
		# Add new user if not already in the database
		user_in_db = User(
			user_id = json_user_id,
			username = json_username,
			email = json_email,
		)
		db.session.add(user_in_db)
	else:
		# Update existing user if necessary
		user_in_db.username = json_username
		user_in_db.email = json_email
	db.session.commit()
	
	# check if user is in system
	user_in_db = User.query.filter_by(user_id=user_info.get("sub")).first()
	if user_in_db:
		return {"status": "success", "message": "User successfully added or updated."}
	else:
		return {"status": "failure", "message": "User could not be added or updated."}


# finalizing authentication
@blueprint.route("/callback")
def callback():
	token = oauth.auth0.authorize_access_token()
	session["user"] = token
	
	# take token's components and add the relevant fields to the local user db
	add_user_to_local_db(token)
	
	# redirect to file upload page, like the original application
	return redirect("/file_upload")


# clearing session
@blueprint.route("/logout")
def logout():
	session.clear()
	
	return redirect(
		"https://" + env.get("AUTH0_DOMAIN") + "/v2/logout?" + urlencode(
			{
				"returnTo": url_for("home.home", _external=True),
				"client_id": env.get("AUTH0_CLIENT_ID"),
			},
			quote_via=quote_plus,
		)
	)
