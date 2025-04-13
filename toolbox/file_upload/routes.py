# some parts are written by brian, but attributions to matt for the overall logic
# in the midst of a rewrite for more robust handling of files in general

# base
import os
import uuid

# flask
from flask import render_template, flash, request

# local
from toolbox.file_upload import blueprint
from toolbox.file_upload.methods import *

# create uploads directory if it doesn't already exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@blueprint.before_request
def create_user_directory():
    # cleans out empty directories before creating a new UUID-dir for each request
    remove_empty_dirs(UPLOAD_FOLDER)
    request.uuid = str(uuid.uuid4())  # Generate a new UUID
    request.upload_path = os.path.join(UPLOAD_FOLDER, request.uuid)
    os.makedirs(request.upload_path, exist_ok=True)  # Create directory

@blueprint.route("/file_upload", methods=["GET", "POST"])
def file_upload():
    # check if user is logged in, redirecting back to the homepage if not
    if check_redirect := check():
        return check_redirect
    
    # initialized boolean flags to check if both forms are submitted
    data_submitted = False
    videos_submitted = False
    
    # On submit of both fields
    if data_submitted and videos_submitted:
        add_session_to_db(request.uuid)
    
    # Render the file upload page
    return render_template("file_upload/file_upload.html", is_admin=is_admin(), data_submitted=data_submitted, videos_submitted=videos_submitted)
