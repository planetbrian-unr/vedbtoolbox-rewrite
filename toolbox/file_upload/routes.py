# base
from io import BytesIO
import os
import requests
import zipfile

# flask and its plugins
from flask import render_template, redirect, url_for, session, request, flash

# pip
from urllib.request import Request, urlopen

# local
from toolbox.file_upload import blueprint
from toolbox.file_upload.forms import DatabraryURLForm, OSFURLForm

def check():
    # If the session is not available AKA the user is not logged in, redirect to home page
    if not session:
        return redirect("/")
    # else do nothing
    return None

# Downloads video files from a Databrary URL
def download_databrary_videos(link: str) -> bytes:
    headers = {
    'Accept': 'text/html, */*; q=0.01, gzip, deflate, br, zstd, en-US,en;q=0.9',
    'Referer': 'https://nyu.databrary.org/volume/1612/slot/65955/zip/false',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    }

    req = Request(link, headers=headers, timeout=10, verify=True)
    
    return urlopen(req).read()

# Downloads data files from OSF 
def download_osf_data(link: str) -> bytes:
    response = requests.get(link)
    if response.status_code != 200:
        flash('Failed!')
        raise Exception(f"Failed to download file: {response.status_code}")
    return response.content

# Extracts the zip file from the response.
def extract_zip(response) -> bool:
    with zipfile.ZipFile(BytesIO(response)) as zip_file:
        zip_file.extractall(os.path.abspath(os.path.dirname(__file__)))
    return True

# Fetches data from a URL and unzips it
def fetch_and_unzip(url_string: str, download_func):
    try:
        response = download_func(url_string)  # Download the content
        extract_zip(response)  # Extract the zip file
    except Exception as e:
        flash(f"Error processing the URL: {e}", 'error')

@blueprint.route("/file_upload", methods=["GET", "POST"])
def file_upload():
    # Check if the user is logged in
    if (check_redirect := check()):
        return check_redirect  # Redirect if the user is not logged in

    # Instantiate the forms
    databraryurl = DatabraryURLForm()
    osfurl = OSFURLForm()

    # Handle the form submission for Databrary URL form or OSF URL form
    if databraryurl.validate_on_submit():  # If Databrary form is valid
        fetch_and_unzip(databraryurl.url.data, download_databrary_videos)
        flash('Videos from Databrary stored!')

    if osfurl.validate_on_submit():  # If OSF form is valid
        fetch_and_unzip(osfurl.url.data, download_osf_data)
        flash('Data from OSF stored!')

    return render_template("file_upload/file_upload.html", databraryurl=databraryurl, osfurl=osfurl)