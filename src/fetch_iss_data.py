import requests

def fetch_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
