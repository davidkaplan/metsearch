import grequests
import requests
import os, tempfile

_ENDPOINT = 'https://collectionapi.metmuseum.org/public/collection/v1/'
_MAX_RETURN_OBJECTS = 80
_TEMP_DIR = tempfile.gettempdir()
print('Tempdir: ', _TEMP_DIR)

'''
rest.py provides helper methods for making single and batch REST requests to the MET objects API
'''

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

def search(search_term, imagesOnly=False):
    '''
    Get a list of Object IDs for a given search query.
    Args:
        search_term (str): The string to query.
        imagesOnly (optional[bool]): Adds the images only flag to the query. Note: Appears to be unrealiable from the server side.
    Returns:
        statuse_code (int): Response code from server.
        ids (list[int]): List of object ids matching the search query.
    '''
    url = _ENDPOINT + 'search?'
    if imagesOnly:
        url += 'hasImages=true&'
    url += ('q=' + search_term)
    status_code, data = _get(url)
    total = data['total']
    ids = data['objectIDs']
    if total == 0 and ids is None:
        ids = []
    return status_code, ids

def getObject(id):
    '''
    Get the complete record data for a given object.
    Args:
        id (int): The object id to query.
    Returns:  
        statuse_code (int): Response code from server.
        data (dict): Object record as dict from the response JSON payload.
    '''
    url = _ENDPOINT + 'objects/' + str(id)
    status_code, data = _get(url)
    return status_code, data

def getObjects(ids):
    '''
    Process a batch of requests for a list of Objects and return their records from the API.
    Args:
        ids (list[int]): The list of object ids to query.
    Returns:  
        num_errors (int): The number of unsuccessful responses.
        sanitized_responses (list[dict]): List of object records.

    '''
    if ids is None or len(ids) == 0:
        return 0, []
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
            print('    Object: ', ids[i])
            print('    URL: ', requests_list[i])
            print('    Payload: ', response.json())
    return num_errors, sanitized_responses

def searchObjects(search_term, **kwargs):
    '''
    Query the API for a given search term and return the object records.
    Args:
        search_term (str): The string to query.
    Returns:  
        errors (int): The number of query errors.
        objects (list[dict]): List of object records.
    '''
    status_code, ids = search(search_term, **kwargs)
    errors, objects = getObjects(ids)
    return errors, objects

def downloadTempFile(url):
    '''
    Download a url to a temporary file. Useful for caching thumbnail images.
    Args:
        url (str): The url of the file to download.
    Returns:  
        tmp_filename (str): The path of the downloaded file in a system-appropriate tmp location.
    '''
    basename = os.path.basename(url)
    if basename == '':
        return None
    tmp_filename = os.path.join(_TEMP_DIR, basename)
    
    # if it already exists, don't download again
    if os.path.isfile(tmp_filename):
        return tmp_filename
    
    with open(tmp_filename, "wb") as fh:
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        fh.write(response.content)
    return tmp_filename
