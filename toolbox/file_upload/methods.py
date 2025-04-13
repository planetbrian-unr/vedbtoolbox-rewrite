# rm_empty_dirs, check are written by brian
# validate link, download funcs are entirely matt's work
# fetch_&_unzip is a rewrite by brian for more "generalized" handling

# base
import os
import zipfile
from io import BytesIO

# flask
from flask import session, redirect, request

# pip
import requests
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from sqlalchemy.exc import SQLAlchemyError

# local
from toolbox import db
from toolbox.models import User, SessionHistory

# Recursively removes empty (checks) UUID-directories in the given root directory.
def remove_empty_dirs(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            dir_to_check = os.path.join(dirpath, dirname)
            if not os.listdir(str(dir_to_check)):
                os.rmdir(dir_to_check)
                print(f"Deleted empty directory: {dir_to_check}")

# If the session is not available AKA the user is not logged in, redirect to home page. else proceed
def check():
    if not session:
        return redirect("/")
    return None

# returns the admin bool (T/F) from the table
def is_admin():
    user = User.query.filter_by(user_id=session['user']['userinfo']['sub']).first()
    return user.admin

# This function validates that the link submitted is an actual link, and goes to the correct website with downloadable (can't really go further)
def validate_link(link: str, flag: int) -> bool:
    # Extract domain (netloc) from the link
    netloc = urlparse(link).netloc.lower()

    # Match the domain based on the flag using a dictionary
    expected_domains = {
        0: "databrary.org",
        1: "osf.io"
    }
    expected_domain = expected_domains.get(flag)
    if expected_domain is None:
        # Invalid flag value
        return False

    # Ensure the domain matches exactly or is a subdomain
    return netloc == expected_domain or netloc.endswith(f".{expected_domain}")

# Helper function to download video files from a Databrary URL
def download_databrary_videos(link: str) -> bytes:
    headers = {
        'Accept': 'text/html, */*; q=0.01, gzip, deflate, br, zstd, en-US, en; q=0.9',
        'Referer': 'https://databrary.org/volume/1612/slot/65955/zip/false',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    }
    return urlopen(Request(link, headers=headers)).read()

# Helper function to download data files from OSF
def download_osf_data(link: str) -> bytes:
    response = requests.get(link)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")
    return response.content

# Helper function to unzip content into a specified directory (likely the UUID folder)
def fetch_and_unzip(download_func, url_string: str, unzip_to: str) -> str:
    try:
        # Download the content (from URL)
        if url_string.startswith("https"):  # Assuming a URL starts with 'https'
            # Download the content
            if download_func == download_databrary_videos:
                response = download_func(url_string)
            elif download_func == download_osf_data:
                response = download_func(url_string)
            else:
                raise Exception("Unknown download function")

            # Unzip the content to the specified directory
            with zipfile.ZipFile(BytesIO(response)) as zip_file:
                zip_file.extractall(unzip_to)
        else:  # It's assumed to be a local file path
            # Read the zip file from the local path
            with open(url_string, 'rb') as local_file:
                with zipfile.ZipFile(local_file) as zip_file:
                    zip_file.extractall(unzip_to)

        return unzip_to  # Return the path where files are unzipped

    except Exception as e:
        return str(e)  # Return error message

# Add new session to database (after successful dual upload)
def add_session_to_db(uuidfolder: str):
    try:
        new_session = SessionHistory (
            session_id = uuidfolder,  # created folder. will have files in it and thus will not be deleted during create_user_directory()
            user_id = session['user']['userinfo']['sub']    # gets user_id (auth0|...) for database integrity
        )
        db.session.add(new_session)
        db.session.commit()
        return {"status": "success", "message": "Session successfully added to DB."}
    except SQLAlchemyError as e:
        # Handle database-related errors
        db.session.rollback()
        return {"status": "error", "message": "An error occurred while interacting with the database."}

    except Exception as e:
        # Handle other errors
        return {"status": "error", "message": "An unexpected error occurred."}
