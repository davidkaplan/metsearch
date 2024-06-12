import rest
import pprint
import time

def test_search():
    s = 'deluge'
    status_code, ids = rest.search(s)
    print(status_code)
    print(ids)

def test_objects():
    s = 'deluge'
    errors, objects = rest.searchObjects(s)
    pprint.pp(objects[0])
    print('Number of Objects:', len(objects))
    print('Number of failed requests:', errors)

if __name__ == '__main__':
    start = time.time()
    #test_search()
    test_objects()
    print('elapsed:', (time.time() - start))