# flask
from flask import Blueprint

blueprint = Blueprint(
    "visualizer_bp", __name__,
    template_folder="templates",
    static_folder="static"
)
