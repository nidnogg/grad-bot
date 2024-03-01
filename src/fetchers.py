from bs4 import BeautifulSoup
import requests
import json
from helpers import checksum_diff


def check_ufsc():
    try:
        url = "https://pgcin.ufsc.br/processos-seletivos/"
        print(f"Fetching JSON from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data_node = soup.find(id="menu-processo-seletivo")
            if data_node is None:
                data_node = soup.find(id="menu--processo-seletivo")
            data = data_node.text
            payload = json.dumps(data, sort_keys=True)
            print(
                f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version."
            )
            if checksum_diff("ufsc", payload):
                print(f"Changes detected on url {url}")
                return True
            else:
                print(f"No changes detected on url {url}")
                return False
    except Exception:
        print(f"WARNING: ROUTINE BREAKING. Changes detected on url {url}")
        return True


def check_ufsc_antro():
    try:
        url = "https://ppgas.posgrad.ufsc.br/"
        print(f"Fetching JSON from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data_node = soup.find(id="menu-ingresso")
            if data_node is None:
                data_node = soup.find(id="menu--ingresso")
            data = data_node.text
            payload = json.dumps(data, sort_keys=True)
            print(
                f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version."
            )
            if checksum_diff("ufsc_antro", payload):
                print(f"Changes detected on url {url}")
                return True
            else:
                print(f"No changes detected on url {url}")
                return False
    except Exception as err:
        print(f"WARNING: ROUTINE BREAKING. Changes detected on url {url}")
        print(f"Reason: {err}")
        return True


def check_unirio():
    try:
        url = "https://www.unirio.br/ppg-pmus/processos-seletivos-mestrado"
        print(f"Fetching JSON from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find(id="content-core").text
            payload = json.dumps(data, sort_keys=True)
            print(
                f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version."
            )
            if checksum_diff("unirio", payload):
                print(f"Changes detected on url {url}")
                return True
            else:
                print(f"No changes detected on url {url}")
                return False
    except Exception as err:
        print(f"WARNING: ROUTINE BREAKING. Changes detected on url {url}")
        print(f"Error: {err}")
        return True


def check_itau():
    try:
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
            print(
                f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version."
            )
            if checksum_diff("itaucultural", payload):
                print(f"Changes detected on url {url}")
                return True
            else:
                print(f"No changes detected on url {url}")
                return False

        else:
            print(f"Request failed with status code: {response.status_code}")
            return True
    except Exception:
        print(f"Changes detected on url {url}, routine breaking")
        return True


def check_ufop():
    try:
        url = "https://turismoepatrimonio.ufop.br/processo-seletivo"
        print(f"Fetching JSON from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find(id="columns").text
            payload = json.dumps(data, sort_keys=True)
            print(
                f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version."
            )
            if checksum_diff("ufop", payload):
                print(f"Changes detected on url {url}")
                return True
            else:
                print(f"No changes detected on url {url}")
                return False
    except Exception as err:
        print(f"WARNING: ROUTINE BREAKING. Changes detected on url {url}")
        print(f"Error: {err}")
        return True


def check_fau():
    try:
        url = "https://pgpp.fau.ufrj.br/"
        print(f"Fetching JSON from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data_nodes = soup.find_all("div", {"class": "main row home"})
            data = ""
            for node in data_nodes:
                data += node.text
            payload = json.dumps(data, sort_keys=True)
            print(
                f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version."
            )
            if checksum_diff("fau", payload):
                print(f"Changes detected on url {url}")
                return True
            else:
                print(f"No changes detected on url {url}")
                return False
    except Exception as err:
        print(f"WARNING: ROUTINE BREAKING. Changes detected on url {url}")
        print(f"Error: {err}")
        return True


def check_iphan_base():
    try:
        url = "http://portal.iphan.gov.br/pep"
        print(f"Fetching JSON from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find(id="container2").text
            payload = json.dumps(data, sort_keys=True)
            print(
                f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version."
            )
            if checksum_diff("iphan_base", payload):
                print(f"Changes detected on url {url}")
                return True
            else:
                print(f"No changes detected on url {url}")
                return False
    except Exception as err:
        print(f"WARNING: ROUTINE BREAKING. Changes detected on url {url}")
        print(f"Error: {err}")
        return True


def check_iphan_patri():
    try:
        url = "http://portal.iphan.gov.br/pep/pagina/detalhes/1827"
        print(f"Fetching JSON from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find(id="master").text
            payload = json.dumps(data, sort_keys=True)
            print(
                f"Successfully fetched payload data from {url}\nNow comparing payload with latest local version."
            )
            if checksum_diff("iphan_patri", payload):
                print(f"Changes detected on url {url}")
                return True
            else:
                print(f"No changes detected on url {url}")
                return False
    except Exception as err:
        print(f"WARNING: ROUTINE BREAKING. Changes detected on url {url}")
        print(f"Error: {err}")
        return True


# Testing routines
# check_ufsc()
# check_ufsc_antro()
# check_ufop()
# check_fau()
# check_iphan_base()
# check_iphan_patri()
