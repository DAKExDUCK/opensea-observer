import requests


def req(name):
    url = f"https://api.opensea.io/api/v1/collection/{name}"
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers)

    return r.status_code, r.json()