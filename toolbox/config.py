import os

class Config():
	CSRF_ENABLED = True
	
	# Set up the App SECRET_KEY
	SECRET_KEY = os.urandom(24)
	
	# This will create a file in <app> FOLDER
	SQLALCHEMY_DATABASE_URI = "sqlite:///project.sqlite"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
