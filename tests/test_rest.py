import unittest
import pprint
import time

from metsearch import rest

class Test_Rest(unittest.TestCase):
    def setUp(self):
        self.start_time = time.time()

    def tearDown(self):
        print('elapsed:', (time.time() - self.start_time))

    def test_search(self):
        s = 'deluge'
        status_code, ids = rest.search(s)
        print(status_code)
        print(ids)
        self.assertEqual(status_code, 200)

    def test_objects(self):
        s = 'deluge'
        errors, objects = rest.searchObjects(s)
        pprint.pp(objects[0])
        print('Number of Objects:', len(objects))
        print('Number of failed requests:', errors)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()