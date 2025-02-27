from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    # Define the relationship to Session_History_URL
    session_history_url = relationship("Session_History_URL", backref="user", lazy=True)
    session_histories_filepath = relationship("Session_History_Filepath", backref="user", lazy=True)

class Session_History_URL(db.Model):
    __tablename__ = "session_history_url"  # Use snake_case for table name
    
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, ForeignKey("users.user_id"), nullable=False)
    osf_url = db.Column(db.String, nullable=False)
    databrary_url = db.Column(db.String, nullable=False)

    # Define the backref to access the user from the session history model
    user = relationship("User", backref="session_histories_url", lazy=True)

class Session_History_Filepath(db.Model):
    __tablename__ = "session_history_filepath"  # Use snake_case for table name
    
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, ForeignKey("users.user_id"), nullable=False)
    data_filepath = db.Column(db.String, nullable=False)
    video_filepath = db.Column(db.String, nullable=False)

    # Define the backref to access the user from the session history model
    user = relationship("User", backref="session_histories_filepath", lazy=True)
