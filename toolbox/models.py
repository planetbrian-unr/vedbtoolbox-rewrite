from toolbox import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(db.Model):
	__tablename__ = "users"

	# user credentials, ripped from auth0 json
	user_id = db.Column(db.String, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	admin = db.Column(db.Boolean, nullable=False, default=False)

	# Define relationships to session histories (URLs and filepaths)
	session_histories = relationship("SessionHistory", backref="user", lazy=True)


class SessionHistory(db.Model):
	__tablename__ = "session_history"

	# metadata
	session_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.String, ForeignKey("users.user_id"), nullable=False)
	session_name = db.Column(db.String, nullable=True, default="VEDB Session")

	# data
	osf_url = db.Column(db.String, nullable=True)
	data_filepath = db.Column(db.String, nullable=True)

	# videos
	databrary_url = db.Column(db.String, nullable=True)
	video_filepath = db.Column(db.String, nullable=True)
