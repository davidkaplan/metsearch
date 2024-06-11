from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QAbstractItemView, QTableWidgetItem, QHeaderView

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

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Preview', 'Title', 'Artist', 'Year'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.Stretch)
        default_width = self.header.sectionSize(0)
        self.header.setDefaultSectionSize(default_width)
        self.header.setSectionResizeMode(QHeaderView.Interactive)
        self.header.resizeSection(0, 50)

        self.table.setSortingEnabled(True)
        self.header.setStretchLastSection(True)
        self.header.setSortIndicatorShown(True)

        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.setLayout(self.main_layout)
        self.resize(600, 600)

    def updateTable(self, items):
        self.table.clearContents()
        self.table.setRowCount(len(items))

        for i, item in enumerate(items):
            try:
                self.table.setItem(i, 1, QTableWidgetItem(item['title']))
                self.table.setItem(i, 2, QTableWidgetItem(item['artistDisplayName']))
                self.table.setItem(i, 3, QTableWidgetItem(item['objectEndDate']))
            except KeyError as e:
                print('KeyError:' + str(e), item)

        #self.table.resizeColumnsToContents()
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
