# matt and brian's work

# base
import os

# flask and its plugins
from flask import render_template, session, redirect

# local
from flaskr.visualizer import blueprint

UPLOAD_FOLDER = 'uploads'

@blueprint.route("/visualizer")
def visualizer():
    upload_path = os.path.join(UPLOAD_FOLDER, session['upload_uuid'])

    eye0_path = f"/{upload_path}/eye0.mp4" if os.path.exists(os.path.join(upload_path, 'eye0.mp4')) else None
    eye1_path = f"/{upload_path}/eye1.mp4" if os.path.exists(os.path.join(upload_path, 'eye1.mp4')) else None
    world_path = f"/{upload_path}/world.mp4" if os.path.exists(os.path.join(upload_path, 'world.mp4')) else None

    return render_template("visualizer/visualizer.html",
                           eye0_path=eye0_path,
                           eye1_path=eye1_path,
                           world_path=world_path)

@blueprint.route("/return_to_file_upload")
def return_to_file_upload():
    session.pop('upload_uuid', None)
    return redirect("/file_upload")
