import sys
from PySide6.QtWidgets import QApplication

import view

def run():
    app = QApplication(sys.argv)
    window = view.MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run()