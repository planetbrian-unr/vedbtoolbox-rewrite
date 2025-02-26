from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    # Define the relationship to Session_History
    session_histories = relationship("Session_History", backref="user", lazy=True)

class Session_History(db.Model):
    __tablename__ = "session_history"  # Use snake_case for table name
    
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, ForeignKey("users.user_id"), nullable=False)  # Corrected FK reference
    osf_url = db.Column(db.String, nullable=False)
    databrary_url = db.Column(db.String, nullable=False)

    # You can also define a backref to access the user from the session history model
    user = relationship("User", backref="session_histories", lazy=True)