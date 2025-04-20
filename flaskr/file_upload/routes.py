# written by brian, with inspiration from matt's original design (the variable-checking)
# in the midst of a rewrite for more robust handling of files in general

# base
import uuid

# flask
from flask import render_template, flash, request, redirect, jsonify
from flask_login import current_user

# local
from flaskr.file_upload import blueprint
from flaskr.file_upload.forms import *
from flaskr.file_upload.methods import *

# create uploads directory if it doesn't already exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@blueprint.before_request
def create_user_directory():
    # Only generate a new UUID if it's not already in the session
    if 'upload_uuid' not in session:
        session['upload_uuid'] = str(uuid.uuid4())
    request.uuid = session['upload_uuid']

    # designate an upload folder, creating it if it doesn't exist
    request.upload_path = os.path.join(UPLOAD_FOLDER, request.uuid)
    if not os.path.exists(request.upload_path):
        remove_empty_dirs(UPLOAD_FOLDER)
        os.makedirs(request.upload_path, exist_ok=True)

    print(f"Using this folder: {request.upload_path}")

@blueprint.route("/file_upload", methods=["GET", "POST"])
def file_upload():
    if not current_user.is_authenticated:
        return redirect("/")
    
    databraryurl = DatabraryURLForm()
    osfurl = OSFURLForm()
    visualizer_button = EnterVisualizer()
    reset_button = ResetFileUpload()
    
    data_submitted = False
    videos_submitted = False
    
    if databraryurl.validate_on_submit() and databraryurl.dtb_submit.data:
        dtb_extraction_path = fetch_and_unzip(download_databrary_videos, databraryurl.dtb_url.data, request.upload_path)
        
        if "Error" in dtb_extraction_path:
            flash(f"Error processing Databrary files: {dtb_extraction_path}", 'error')
        else:
            if files_exist(request.upload_path, ['.mp4', '.csv']):
                flash(f"Videos from Databrary stored in: {dtb_extraction_path}")
                videos_submitted = True
            else:
                flash("No files were uploaded for Databrary.", 'error')
    
    if osfurl.validate_on_submit() and osfurl.osf_submit.data:
        osf_extraction_path = fetch_and_unzip(download_osf_data, osfurl.osf_url.data, request.upload_path)
        
        if "Error" in osf_extraction_path:
            flash(f"Error processing OSF files: {osf_extraction_path}", 'error')
        else:
            if files_exist(request.upload_path, ['.pldata', '.npy', '.npz', '.yaml', '.intrinsics', '.extrinsics']):
                flash(f"Data from OSF stored in: {osf_extraction_path}")
                data_submitted = True
            else:
                flash("No files were uploaded for OSF.", 'error')
    
    if visualizer_button.validate_on_submit() and visualizer_button.submit.data and data_submitted and videos_submitted:
        add_session_to_db(request.uuid)
        session.pop('upload_uuid', None)
        return redirect("/visualizer")
    
    if reset_button.validate_on_submit() and reset_button.reset.data:
        clear_directory(request.upload_path)
        data_submitted = False
        videos_submitted = False
    
    return render_template("file_upload/file_upload.html",
                           is_admin=is_admin(),
                           data_submitted=data_submitted,
                           videos_submitted=videos_submitted,
                           databraryurl=databraryurl,
                           osfurl=osfurl,
                           visualizer_button=visualizer_button,
                           reset_button=reset_button
                           )


@blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'filepond' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['filepond']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file to the user's uuid upload folder
    file.save(os.path.join(request.upload_path, file.filename))
    
    return jsonify({'id': file.filename})
