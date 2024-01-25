import os
import requests
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

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Retrieve JSON response
        # Process 'data' as needed
        # print(data)
        # Formatted
        payload = data
        print(f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version.")
        compare_with_older("itaucultural", payload)
    else:
        print(f"Request failed with status code: {response.status_code}")

def compare_with_older(site, payload):
    # Prints nothing
    print(payload)
    script_directory = os.path.dirname(os.path.realpath(__file__))
    watched_folder = os.path.join(script_directory, "watched")
    watched_file = os.path.join(watched_folder, f"{site}_latest.json")
    try:
        with open(watched_file, "r") as latest_file:
            content = latest_file.read()
            print(content)
    except FileNotFoundError:
        print("Currently not watched. Generating latest version...")
         # Ensure the directory structure exists
        if not os.path.exists(watched_folder):
            os.makedirs(watched_folder)
        with open(watched_file, "w") as latest_file:
            # Doesnt print anything
            print(payload)
            json.dump(payload, latest_file, indent=2)
            print("Latest version generated and saved.")

fetch_itau()
