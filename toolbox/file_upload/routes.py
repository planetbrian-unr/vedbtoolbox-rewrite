# some parts are written by brian, but attributions to matt for the overall logic
# in the midst of a rewrite for more robust handling of files in general

# base
import os
import uuid

# flask
from flask import render_template, flash, request

# local
from toolbox.file_upload import blueprint
from toolbox.file_upload.forms import *
from toolbox.file_upload.methods import *

# create uploads directory if it doesn't already exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@blueprint.before_request
def create_user_directory():
    # Only generate a new UUID if it's not already in the session
    if 'upload_uuid' not in session:
        session['upload_uuid'] = str(uuid.uuid4())

    uuid_str = session['upload_uuid']
    session_upload_path = os.path.join(UPLOAD_FOLDER, uuid_str)

    # Create path if it doesn't exist yet
    if not os.path.exists(session_upload_path):
        remove_empty_dirs(UPLOAD_FOLDER)
        os.makedirs(session_upload_path, exist_ok=True)

    request.upload_path = session_upload_path
    request.uuid = uuid_str
    
    print(f"Using this folder: {request.upload_path}")

@blueprint.route("/file_upload", methods=["GET", "POST"])
def file_upload():
    # check if user is logged in, redirecting back to the homepage if not
    if check_redirect := check():
        return check_redirect
    
    # forms
    databraryurl = DatabraryURLForm()
    osfurl = OSFURLForm()
    visualizer_button = EnterVisualizer()

    # initialized boolean flags dictionary to check if both forms are submitted
    data_submitted = False
    videos_submitted = False
    
    # url handling
    if databraryurl.validate_on_submit():  # If Databrary form is valid
        if not validate_link(databraryurl.url.data, 0):  # Validate the link for Databrary (flag 0)
            flash("Video URL not valid! It should be a valid Databrary URL.")

        # Attempt to fetch and unzip Databrary video files
        dtb_extraction_path = fetch_and_unzip(download_databrary_videos, databraryurl.url.data, request.upload_path)
        
        if "Error" in dtb_extraction_path:
            flash(f"Error processing Databrary files: {dtb_extraction_path}", 'error')
        else:
            flash(f"Videos from Databrary stored in: {dtb_extraction_path}")
            videos_submitted = True
    
    if osfurl.validate_on_submit():  # If OSF form is valid
        if not validate_link(osfurl.url.data, 1):  # Validate the link for OSF (flag 1)
            flash("Data URL not valid! It should be a valid OSF URL.")

        # Attempt to fetch and unzip OSF data files
        osf_extraction_path = fetch_and_unzip(download_osf_data, osfurl.url.data, request.upload_path)
        
        if "Error" in osf_extraction_path:
            flash(f"Error processing OSF files: {osf_extraction_path}", 'error')
        else:
            flash(f"Data from OSF stored in: {osf_extraction_path}")
            data_submitted = True
    
    # On submit of both fields AKA dictionary has all True values
    if visualizer_button.validate_on_submit():
        add_session_to_db(request.uuid)
        session.pop('upload_uuid', None)
    
    # Render the file upload page
    return render_template("file_upload/file_upload.html",
        is_admin=is_admin(),
        data_submitted=data_submitted,
        videos_submitted=videos_submitted,
        databraryurl=databraryurl,
        osfurl=osfurl,
        visualizer_button=visualizer_button
    )
