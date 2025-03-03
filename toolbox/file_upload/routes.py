# base
import os

# flask and its plugins
from flask import render_template, redirect, url_for, session, request, current_app

# local
from toolbox.file_upload import blueprint
from toolbox.file_upload.forms import DatabraryURLForm, OSFURLForm

def check():
    # If the session is not available AKA the user is not logged in, redirect to home page
    if not session:
        return redirect("/")
    # Return None if the user is logged in
    else:
        return None

def fetch_and_unzip_videos(url_string):
    return 0

def fetch_and_unzip_data(url_string):
    return 0


@blueprint.route("/file_upload", methods=["GET", "POST"])
def file_upload():
    # checks if logged in
    check_redirect = check()
    if check_redirect:
        return check_redirect  # Redirect if the user is not logged in
    
    if request.method == 'POST':
        f = request.files.get('file')
        file_path = os.path.join(current_app.config['UPLOADED_PATH'], f.filename)
        f.save(file_path)
    
    return render_template("file_upload/file_upload.html")
