import os
import requests
import hashlib
import json
from bs4 import BeautifulSoup

def fetch_itau():
    print("Fetching from itau...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://escola.itaucultural.org.br/",
        "X-Organization-Name": "escola_ic",
        "Origin": "https://escola.itaucultural.org.br",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Connection": "keep-alive",
        "If-None-Match": 'W/"a535e7011691118f7a9ece9cf7178f13"',
    }

    url = "https://lms.itaucultural.org.br/api/v1/courses?page=1&per_page=24&course_type=with_mediator" 
    print("https://escola.itaucultural.org.br/")
    print("Fetching JSON from ", url)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Retrieve JSON response
        payload = data
        print(f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version.")
        compare_with_older("itaucultural", payload)
    else:
        print(f"Request failed with status code: {response.status_code}")

def compare_with_older(site, payload):
    """
    Compares the checksum of the current payload with the latest stored payload for a given site.

    Parameters:
        site (str): Name of the site for comparison.
        payload (dict or list): Data to be compared.

    Raises:
        FileNotFoundError: If latest file for the site is not found.

    Returns:
        None
    """
    script_directory = os.path.dirname(os.path.realpath(__file__))
    watched_folder = os.path.join(script_directory, "watched")
    latest_filepath = os.path.join(watched_folder, f"{site}_latest.json")
    current_filepath = os.path.join(watched_folder, f"{site}_current.json")

    try:
        with open(latest_filepath, "r+") as latest_file:
            with open(current_filepath, "w") as current_file:
                # Populate current file to compare checksums
                json.dump(payload[0], current_file, indent=2)
                current_file.close()
                latest_file.seek(0)  # Move cursor to the beginning of the file
                latest_file.truncate()  # Clear the file
                json.dump(payload[0], latest_file, indent=2)  # Rewrite latest file
                latest_file.flush()  # Flush changes to disk

    except FileNotFoundError:
        print("Currently not watched. Generating latest version...")
        # Ensure the directory structure exists
        if not os.path.exists(watched_folder):
            os.makedirs(watched_folder)
        with open(latest_filepath, "w") as latest_file:
            json.dump(payload, latest_file, indent=2, sort_keys=True)
            print("Latest version generated and saved.")

    # Perform the actual comparison
    current_checksum = calculate_checksum(current_filepath)
    latest_checksum = calculate_checksum(latest_filepath)
    print(f"Checksum (SHA-256) of current file: {current_checksum}")
    print(f"Checksum (SHA-256) of latest file: {latest_checksum}")


    if current_checksum != latest_checksum:
        print("Checksum difference found:")
        print(f"Latest checksum: {latest_checksum}\nCurrent checksum: {current_checksum}")
        print("Replacing latest file")
        with open(latest_filepath, "w") as latest_file:
            json.dump(payload[0], latest_file, indent=2, sort_keys=True)

def calculate_checksum(filepath):
    """Calculate checksum of a file."""
    try:
        with open(filepath, 'rb') as file:
            return hashlib.md5(file.read()).hexdigest()
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return None
fetch_itau()
