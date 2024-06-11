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
    objects = rest.searchObjects(s)
    print('Number of Objects:', len(objects))
    pprint.pp(objects[0])

if __name__ == '__main__':
    start = time.time()
    #test_search()
    test_objects()
    print('elapsed:', (time.time() - start))