# base
import uuid
import os
import zipfile
from io import BytesIO

# flask
from flask import session, redirect, url_for

# pip
import requests
from urllib.request import Request, urlopen

def check():
    # If the session is not available AKA the user is not logged in, redirect to home page
    if not session:
        return redirect("/")
    # else do nothing
    return None

# This function validates that the link submitted is an actual link, and goes to the correct website with downloadable (can't really go further)
def validate_link(link: str, flag: int) -> bool:
    if "." not in link:
        return False
    if "osf.io" not in link and flag == 1:
        return False
    if "nyu.databrary.org" not in link and flag == 0:
        return False
    # Passes first check, still forced to hit others (exception)
    return True

# Helper function to download video files from a Databrary URL
def download_databrary_videos(link: str) -> bytes:
    headers = {
        'Accept': 'text/html, */*; q=0.01, gzip, deflate, br, zstd, en-US, en; q=0.9',
        'Referer': 'https://nyu.databrary.org/volume/1612/slot/65955/zip/false',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    }
    req = Request(link, headers=headers, timeout=10, verify=True)
    return urlopen(req).read()

# Helper function to download data files from OSF
def download_osf_data(link: str) -> bytes:
    response = requests.get(link)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")
    return response.content

# Helper function to unzip content into a unique directory
def fetch_and_unzip(download_func, url_string: str) -> str:
    try:
        # Generate a random folder name
        base_directory = "uploads"
        random_folder_name = str(uuid.uuid4())

        # Ensure the directory exists
        os.makedirs(os.path.join(base_directory, random_folder_name))

        # Download the content
        response = download_func(url_string)

        # Unzip the content to the specified directory
        with zipfile.ZipFile(BytesIO(response)) as zip_file:
            zip_file.extractall(os.path.join(base_directory, random_folder_name))

        return os.path.join(base_directory, random_folder_name)
    except Exception as e:
        return str(e)  # Return error message
