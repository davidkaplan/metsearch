import sys
from PySide6.QtWidgets import QApplication
import pprint 

import rest
import view

def test_show():
    app = QApplication(sys.argv)
    window = view.MainWindow()
    window.show()
    sys.exit(app.exec())

def test_populate():
    app = QApplication(sys.argv)
    window = view.MainWindow()
    window.show()
    s = 'stone'
    errors, artworks = rest.searchObjects(s)
    artworks = artworks
    window.updateTable(artworks)
    sys.exit(app.exec())


if __name__ == "__main__":
    #test_show()
    test_populate()