# flask
from flask import session, redirect

def check():
    # If the session is available AKA the user is logged in, redirect to file_upload
    if session:
        return redirect("/file_upload")
    # else do nothing
    return None