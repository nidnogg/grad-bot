from bs4 import BeautifulSoup
import requests
import json
from helpers import checksum_diff

def check_ufsc():
    url = 'https://pgcin.ufsc.br/processos-seletivos/'
    print(f"Fetching JSON from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find(id='menu-processo-seletivo').text
        payload = json.dumps(data, sort_keys = True)
        print(f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version.")
        if checksum_diff("ufsc", payload):
            print(f"Changes detected on url {url}")
            return True
        else:
            print(f"No changes detected on url {url}")
            return False

def check_ufsc_antro():
    url = "https://ppgas.posgrad.ufsc.br/"
    print(f"Fetching JSON from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find(id='menu-ingresso').text
        payload = json.dumps(data, sort_keys = True)
        print(f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version.")
        if checksum_diff("ufsc_antro", payload):
            print(f"Changes detected on url {url}")
            return True
        else:
            print(f"No changes detected on url {url}")
            return False

def check_unirio():
    url = 'https://www.unirio.br/ppg-pmus/processos-seletivos-mestrado'
    print(f"Fetching JSON from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find(id='content-core').text
        payload = json.dumps(data, sort_keys = True)
        print(f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version.")
        if checksum_diff("unirio", payload):
            print(f"Changes detected on url {url}")
            return True
        else:
            print(f"No changes detected on url {url}")
            return False

def check_itau():
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
        payload = data[0]
        print(f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version.")
        if checksum_diff("itaucultural", payload):
            print(f"Changes detected on url {url}")
            return True
        else:
            print(f"No changes detected on url {url}")
            return False

    else:
        print(f"Request failed with status code: {response.status_code}")