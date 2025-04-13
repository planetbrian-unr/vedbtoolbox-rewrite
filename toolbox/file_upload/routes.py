# written by brian, with inspiration from matt's original design (the variable-checking)
# in the midst of a rewrite for more robust handling of files in general

# base
import uuid

# flask
from flask import render_template, flash, request, redirect, jsonify

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
    request.uuid = session['upload_uuid']

    # designate an upload folder, creating it if it doesn't exist
    request.upload_path = os.path.join(UPLOAD_FOLDER, request.uuid)
    if not os.path.exists(request.upload_path):
        remove_empty_dirs(UPLOAD_FOLDER)
        os.makedirs(request.upload_path, exist_ok=True)
    
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
    reset_button = ResetFileUpload()

    # initialized boolean flags dictionary to check if both forms are submitted
    data_submitted = False
    videos_submitted = False
    
    # url handling
    if databraryurl.validate_on_submit() and databraryurl.dtb_submit.data:  # If Databrary form is valid
        # Attempt to fetch and unzip Databrary video files
        dtb_extraction_path = fetch_and_unzip(download_databrary_videos, databraryurl.dtb_url.data, request.upload_path)
        
        if "Error" in dtb_extraction_path:
            flash(f"Error processing Databrary files: {dtb_extraction_path}", 'error')
        else:
            flash(f"Videos from Databrary stored in: {dtb_extraction_path}")
            videos_submitted = True
    
    if osfurl.validate_on_submit() and osfurl.osf_submit.data:  # If OSF form is valid
        # Attempt to fetch and unzip OSF data files
        osf_extraction_path = fetch_and_unzip(download_osf_data, osfurl.osf_url.data, request.upload_path)
        
        if "Error" in osf_extraction_path:
            flash(f"Error processing OSF files: {osf_extraction_path}", 'error')
        else:
            flash(f"Data from OSF stored in: {osf_extraction_path}")
            data_submitted = True

    # On submit of both fields AKA dictionary has all True values
    if visualizer_button.validate_on_submit() and visualizer_button.submit.data and data_submitted and videos_submitted:
        print("files submitted!")
        add_session_to_db(request.uuid)
        session.pop('upload_uuid', None)
        return redirect("/visualizer")
    
    # On submit, it will delete whatever has been uploaded to request.upload_path folder
    if reset_button.validate_on_submit() and reset_button.reset.data:
        print("Reset form submitted!")
        clear_directory(request.upload_path)
        data_submitted = False
        videos_submitted = False
        
    # Render the file upload page
    return render_template("file_upload/file_upload.html",
        is_admin=is_admin(),
        
        # flags and other variables
        data_submitted=data_submitted,
        videos_submitted=videos_submitted,
        
        # forms and buttons
        databraryurl=databraryurl,
        osfurl=osfurl,
        visualizer_button=visualizer_button,
        reset_button=reset_button
    )

@blueprint.route('/upload', methods=['POST'])
def upload_file():
    print("Reached the upload route!")
    
    if 'filepond' not in request.files:
        print("error here 1")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['filepond']
    if file.filename == '':
        print("error here 2")
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to the user's uuid upload folder
    file.save(os.path.join(request.upload_path, file.filename))

    print("made it")
    return jsonify({'id': file.filename})
