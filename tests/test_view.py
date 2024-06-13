import sys
import unittest
from PySide6.QtWidgets import QApplication
import pprint 

from metsearch import rest
from metsearch import view

app = QApplication(sys.argv)

class Test_View(unittest.TestCase):

    def setUp(self):
        self.app = app.instance()

    def tearDown(self):
        self.app.closeAllWindows()
        self.app.exit()

    def test_show(self):
        window = view.MainWindow()
        window.show()
        self.assertTrue(True)

    def test_populate(self):
        window = view.MainWindow()
        window.show()
        s = 'deluge'
        errors, artworks = rest.searchObjects(s)
        artworks = artworks
        window.updateTable(artworks)
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()