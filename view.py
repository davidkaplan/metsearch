
import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MET Search')

        self.label = QLabel('Search')
        self.search = QLineEdit('')
        self.button = QPushButton("Search")

        self.searchbar_layout = QHBoxLayout()
        self.searchbar_layout.addWidget(self.label)
        self.searchbar_layout.addWidget(self.search)
        self.searchbar_layout.addWidget(self.button)

        self.table = QTableWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.searchbar_layout)
        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)