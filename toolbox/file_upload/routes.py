# some parts are written by brian, but attributions to matt for the overall logic
# in the midst of a rewrite for more robust handling of files in general

# base
import os
import uuid

# flask
from flask import render_template, flash, request

# local
from toolbox.file_upload import blueprint
from toolbox.file_upload.forms import DatabraryURLForm, OSFURLForm
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
    
    # Instantiate the forms
    databraryurl = DatabraryURLForm()
    osfurl = OSFURLForm()

    # boolean flags to check if both forms are submitted
    databrary_submitted = False
    osf_submitted = False

    ### Databrary handling
    # URL
    if databraryurl.validate_on_submit():  # If Databrary form is valid
        if not validate_link(databraryurl.url.data, 0):  # Validate the link for Databrary (flag 0)
            flash("Video URL not valid! It should be a valid Databrary URL.")
            return render_template("file_upload/file_upload.html", databraryurl=databraryurl, osfurl=osfurl)

        # Attempt to fetch and unzip Databrary video files
        extraction_path = fetch_and_unzip(download_databrary_videos, databraryurl.url.data)

        if "Error" in extraction_path:
            flash(f"Error processing Databrary files: {extraction_path}", 'error')
        else:
            flash(f"Videos from Databrary stored in: {extraction_path}")
            
        databrary_submitted = True


    ### OSF handling
    # URL
    if osfurl.validate_on_submit():  # If OSF form is valid
        if not validate_link(osfurl.url.data, 1):  # Validate the link for OSF (flag 1)
            flash("Data URL not valid! It should be a valid OSF URL.")
            return render_template("file_upload/file_upload.html", databraryurl=databraryurl, osfurl=osfurl)

        # Attempt to fetch and unzip OSF data files
        extraction_path = fetch_and_unzip(download_osf_data, osfurl.url.data)

        if "Error" in extraction_path:
            flash(f"Error processing OSF files: {extraction_path}", 'error')
        else:
            flash(f"Data from OSF stored in: {extraction_path}")
            
        osf_submitted = True
    
    # user_id value
    sub_value = session['user']['userinfo']['sub']
    
    # Render the file upload page with the forms
    return render_template("file_upload/file_upload.html", databraryurl=databraryurl, osfurl=osfurl)
