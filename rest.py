import requests

_ENDPOINT = 'https://collectionapi.metmuseum.org/public/collection/v1/'

def _get(url):
    r = requests.get(url)
    status_code = r.status_code
    data = r.json()
    return status_code, data

def search(search_term):
    url = _ENDPOINT + 'search?q=' + search_term
    status_code, data = _get(url)
    total = data['total']
    ids = data['objectIDs']
    return status_code, ids

def getObject(id):
    url = _ENDPOINT + 'objects/' + str(id)
    status_code, data = _get(url)
    return status_code, data

def getObjects(ids):
    objects = []
    for id in ids:
        status_code, data = getObject(id)
        objects.append(data)
    return objects

def searchObjects(search_term):
    status_code, ids = search(search_term)
    objects = getObjects(ids)
    return objects