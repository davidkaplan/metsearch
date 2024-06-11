import requests

def test_search():
    s = 'https://collectionapi.metmuseum.org/public/collection/v1/search?q=deluge'
    r = requests.get(s)
    status_code = r.status_code
    data = r.json()
    total = data['total']
    ids = data['objectIDs']
    print(ids)

if __name__ == '__main__':
    test_search()