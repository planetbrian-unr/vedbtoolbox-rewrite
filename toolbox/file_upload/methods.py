# rm_empty_dirs, check are written by brian
# validate link, download funcs are entirely matt's work
# fetch_&_unzip is a rewrite for more "generalized" handling

# base
import os
import zipfile
from io import BytesIO

# flask
from flask import session, redirect, url_for

# pip
import requests
from urllib.request import Request, urlopen


# Recursively removes empty (checks) UUID-directories in the given root directory.
def remove_empty_dirs(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            dir_to_check = os.path.join(dirpath, dirname)
            if not os.listdir(dir_to_check):
                os.rmdir(dir_to_check)
                print(f"Deleted empty directory: {dir_to_check}")

# If the session is not available AKA the user is not logged in, redirect to home page. else proceed
def check():
    if not session:
        return redirect("/")
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
