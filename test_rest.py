import rest

def test_search():
    s = 'deluge'
    status_code, ids = rest.search(s)
    print(status_code)
    print(ids)

if __name__ == '__main__':
    test_search()