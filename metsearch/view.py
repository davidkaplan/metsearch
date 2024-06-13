from PySide6.QtWidgets import QWidget, QTableWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QAbstractItemView, QTableWidgetItem, QHeaderView, QCheckBox
from PySide6.QtCore import QObject, Signal, QThreadPool, QRunnable, QSize
from PySide6.QtGui import QPixmap

from metsearch import rest

_ROW_HEIGHT = 100 # pixels

class ImageDownloaderSignals(QObject):
    finished = Signal()
    result = Signal(str, QTableWidgetItem)

class ImageDownloader(QRunnable):
    def __init__(self, url, tableitem):
        super(ImageDownloader, self).__init__()
        self.url = url
        self.tableitem = tableitem
        self.signals = ImageDownloaderSignals()

    def run(self):
        tmp_file = rest.downloadTempFile(self.url)
        self.signals.result.emit(tmp_file, self.tableitem)
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MET Search')

        self.label = QLabel('Search')
        self.search = QLineEdit('')
        self.hasImageCheckBox = QCheckBox('Has Image')
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.doSearch)

        self.searchbar_layout = QHBoxLayout()
        self.searchbar_layout.addWidget(self.label)
        self.searchbar_layout.addWidget(self.search)
        self.searchbar_layout.addWidget(self.hasImageCheckBox)
        self.searchbar_layout.addWidget(self.searchButton)

        self.table = QTableWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.searchbar_layout)
        self.main_layout.addWidget(self.table)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Preview', 'Title', 'Artist', 'Date'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.Stretch)
        default_width = self.header.sectionSize(0)
        self.header.setDefaultSectionSize(default_width)
        self.header.setSectionResizeMode(QHeaderView.Interactive)
        self.header.resizeSection(0, _ROW_HEIGHT)
        self.table.setIconSize(QSize(_ROW_HEIGHT, _ROW_HEIGHT))

        self.table.setSortingEnabled(True)
        self.header.setStretchLastSection(True)
        self.header.setSortIndicatorShown(True)

        self.table.verticalHeader().setDefaultSectionSize(_ROW_HEIGHT)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.setLayout(self.main_layout)
        self.resize(600, 600)
                                                
        self.threadpool = QThreadPool()

    def updateTable(self, items):
        self.table.clearContents()
        self.table.setRowCount(len(items))

        for i, item in enumerate(items):
            try:
                self.table.setItem(i, 0, QTableWidgetItem())
                self.table.setItem(i, 1, QTableWidgetItem(item['title']))
                self.table.setItem(i, 2, QTableWidgetItem(item['artistDisplayName']))
                self.table.setItem(i, 3, QTableWidgetItem(str(item['objectEndDate'])))
            except KeyError as e:
                print('KeyError:' + str(e), item)

            # Cache Images
            if 'primaryImageSmall' in item:
                url = item['primaryImageSmall']
                if url == '':
                    continue
                tableitem = self.table.item(i, 0)
                worker = ImageDownloader(url, tableitem)
                worker.signals.result.connect(self.updateThumbnail)
                self.threadpool.start(worker)
        
        # reset scroll to top
        self.table.scrollToItem(self.table.item(0, 0))

    def updateThumbnail(self, filename, tableitem):
        if filename and not filename == '':
            thumb_pixmap = QPixmap(filename)
            tableitem.setSizeHint(QSize(_ROW_HEIGHT, _ROW_HEIGHT))
            tableitem.setIcon(thumb_pixmap)

    def doSearch(self):
        search_string = self.search.text()
        if search_string == '':
            return
        hasImage = self.hasImageCheckBox.isChecked()
        errors, artworks = rest.searchObjects(search_string, imagesOnly=hasImage)
        self.updateTable(artworks)

