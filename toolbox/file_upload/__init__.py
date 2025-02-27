from flask import Blueprint

blueprint = Blueprint(
    "file_upload_bp", __name__,
    template_folder="templates",
    static_folder="static"
)
