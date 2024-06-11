import grequests
import requests

_ENDPOINT = 'https://collectionapi.metmuseum.org/public/collection/v1/'

def _get(url):
    r = requests.get(url)
    status_code = r.status_code
    data = r.json()
    return status_code, data

def _object_requests_list(ids):
    requests_list = []
    for id in ids:
        url = _ENDPOINT + 'objects/' + str(id)
        requests_list.append(url)
    return requests_list

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
    requests_list = _object_requests_list(ids)
    reqs = [grequests.get(u) for u in requests_list]
    responses = grequests.map(reqs)
    objects = [response.json() for response in responses]
    return objects

def searchObjects(search_term):
    status_code, ids = search(search_term)
    objects = getObjects(ids)
    return objects