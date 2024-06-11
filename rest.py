import grequests
import requests

_ENDPOINT = 'https://collectionapi.metmuseum.org/public/collection/v1/'
_MAX_RETURN_OBJECTS = 80

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
    ids = ids[:_MAX_RETURN_OBJECTS]
    requests_list = _object_requests_list(ids)
    reqs = [grequests.get(u) for u in requests_list]
    responses = grequests.map(reqs)
    num_errors = 0
    sanitized_responses = []
    for i, response in enumerate(responses):
        try:
            response.raise_for_status()
            sanitized_responses.append(response.json())
        except requests.exceptions.RequestException:
            num_errors += 1
            print('WARNING: Request failed with code ' + str(response.status_code), response)
            print('Object: ', ids[i])
            print('URL: ', requests_list[i])
            print('Payload: ', response.json())
    return num_errors, sanitized_responses

def searchObjects(search_term):
    status_code, ids = search(search_term)
    errors, objects = getObjects(ids)
    return errors, objects