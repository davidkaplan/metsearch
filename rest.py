import requests

_ENDPOINT = 'https://collectionapi.metmuseum.org/public/collection/v1/'

def search(search_term):
    url = _ENDPOINT + 'search?q=' + search_term
    r = requests.get(url)
    status_code = r.status_code
    data = r.json()
    total = data['total']
    ids = data['objectIDs']
    return status_code, ids
