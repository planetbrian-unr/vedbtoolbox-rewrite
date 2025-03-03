import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	# Randomized secret key
	SECRET_KEY = os.urandom(24)
	
	# sqlalchemy stuff
	SQLALCHEMY_DATABASE_URI = "sqlite:///project.sqlite"
	SQLALCHEMY_ECHO = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	# dropzone. allows parallel uploads of only the files types found in the dataset (up to 2GiB per file)
	DROPZONE_MAX_FILE_SIZE = 2048
	DROPZONE_ALLOWED_FILE_CUSTOM = True
	DROPZONE_ALLOWED_FILE_TYPE = '.pldata, .npy, .intrinsics, .extrinsics, .yaml, .DS_Store'
	DROPZONE_ALLOWED_FILE_TYPE += '.mp4, .csv'
	DROPZONE_UPLOAD_MULTIPLE = True
	DROPZONE_PARALLEL_UPLOADS = 4
	DROPZONE_ENABLE_CSRF = True

	# uploads filepath
	UPLOADS_PATH=os.path.join(basedir, 'uploads')
