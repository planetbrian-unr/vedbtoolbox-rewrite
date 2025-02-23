# base
import json
import os

# pip packages
from flask import url_for, session, redirect, render_template
from urllib.parse import quote_plus, urlencode

from . import create_app
from .models import db, User

# home, will render an authenticated user's details, or allow sign-in
def home():
	return render_template("home.html", session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))


# trigger authentication
def login():
	return oauth.auth0.authorize_redirect(
		redirect_uri=url_for("callback", _external=True)
	)


# finalizing authentication
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
	user_in_db = User.query.filter_by(user_id=json_user_id).first()
	if not user_in_db:
		# Add new user if not already in the database
		user_in_db = User(
			user_id=json_user_id,
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
@app.route("/logout")
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
