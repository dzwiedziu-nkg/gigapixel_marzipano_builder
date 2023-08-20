import sys
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QDialog, QPushButton, QFileDialog,
                               QGroupBox)

from flat import TiffImage


class MainWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.settings = QSettings('nkg', 'Tiles')

        self.source_le = None
        self.destination_le = None
        self.tiles_x_le = None
        self.tiles_y_le = None
        self.status_te = None

        self.title_le = None
        self.description_le = None

        self.ti = None

        self.init_ui()

    def init_ui(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        source_file_label = QLabel('Source file:')
        source_file_edit = QLineEdit()
        source_file_dialog = QPushButton('Select')
        source_file_dialog.clicked.connect(self.source_file_clicked)
        self.source_le = source_file_edit

        grid.addWidget(source_file_label, 1, 0)
        grid.addWidget(source_file_edit, 1, 1)
        grid.addWidget(source_file_dialog, 1, 2)

        destination_dir_label = QLabel('Destination:')
        destination_dir_edit = QLineEdit()
        destination_dir_dialog = QPushButton('Select')
        destination_dir_dialog.clicked.connect(self.destination_dir_clicked)
        self.destination_le = destination_dir_edit

        grid.addWidget(destination_dir_label, 2, 0)
        grid.addWidget(destination_dir_edit, 2, 1)
        grid.addWidget(destination_dir_dialog, 2, 2)

        # groupbox
        groupbox = QGroupBox("Settings")
        grid.addWidget(groupbox, 3, 0, 1, 3)

        gb_grid = QGridLayout()
        gb_grid.setSpacing(10)

        tile_x_label = QLabel('Tile X:')
        tile_x_edit = QLineEdit('1024')
        self.tiles_x_le = tile_x_edit
        gb_grid.addWidget(tile_x_label, 1, 0)
        gb_grid.addWidget(tile_x_edit, 1, 1)

        tile_y_label = QLabel('Tile X:')
        tile_y_edit = QLineEdit('1024')
        self.tiles_y_le = tile_y_edit
        gb_grid.addWidget(tile_y_label, 1, 2)
        gb_grid.addWidget(tile_y_edit, 1, 3)

        groupbox.setLayout(gb_grid)
        # end

        analyse_button = QPushButton('Analyse')
        analyse_button.clicked.connect(self.analyse_clicked)

        process_button = QPushButton('Process')
        process_button.clicked.connect(self.process_clicked)

        b_grid = QGridLayout()
        b_grid.setSpacing(10)
        b_grid.addWidget(analyse_button, 1, 0)
        b_grid.addWidget(process_button, 1, 1)
        grid.addLayout(b_grid, 4, 0, 1, 3)

        title_label = QLabel('HTML Title:')
        title_edit = QLineEdit()
        self.title_le = title_edit
        grid.addWidget(title_label, 5, 0)
        grid.addWidget(title_edit, 5, 1, 1, 2)

        description_label = QLabel('HTML Description:')
        description_edit = QLineEdit()
        self.description_le = description_edit
        grid.addWidget(description_label, 6, 0)
        grid.addWidget(description_edit, 6, 1, 1, 2)

        status_label = QLabel('Status:')
        grid.addWidget(status_label, 7, 0, 1, 3)

        status_te = QTextEdit()
        self.status_te = status_te
        grid.addWidget(status_te, 8, 0, 1, 3)

        self.setLayout(grid)

        self.resize(640, 480)
        self.center()
        self.setWindowTitle('Gigapixel panorama splitter for Marzipano.js v0.1')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clear_log(self):
        self.status_te.setText('')

    def append_log(self, text):
        self.status_te.moveCursor(QTextCursor.End)
        self.status_te.insertPlainText(text)

    def source_file_clicked(self):
        home_dir = self.settings.value('open_path', str(Path.home()))
        filters = "TIFF images (*.tif *.tiff);;All files (*.*)"
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, filters)

        if fname[0]:
            self.ti = None
            self.source_le.setText(fname[0])
            self.settings.setValue('open_path', str(Path(fname[0]).parent))
            self.destination_le.setText(str(Path(fname[0]).parent))

    def destination_dir_clicked(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Folder', str(Path(self.source_le.text()).parent))
        if fname:
            self.destination_le.setText(fname)

    def analyse_clicked(self):
        self.clear_log()

        source_file = self.source_le.text()
        ti = TiffImage(source_file)
        self.ti = ti

        self.append_log('File "%s" opened\n' % Path(source_file).name)
        self.append_log('Image width: %d\n' % ti.image.shape[1])
        self.append_log('Image height: %d\n' % ti.image.shape[0])
        gpix = (ti.image.shape[1] * ti.image.shape[0]) / 1000000000.0

        if self.description_le.text().strip() == '':
            description = 'Gigapixel panorama, full resolution: %d x %d (%.1f GPix)' % (ti.image.shape[1], ti.image.shape[0], gpix)
            self.description_le.setText(description)

    def process_clicked(self):
        source_file = self.source_le.text()
        destination_dir = self.destination_le.text()
        if self.ti is None:
            self.ti = TiffImage(source_file)
        tiles_x = int(self.tiles_x_le.text())
        tiles_y = int(self.tiles_y_le.text())
        self.ti.make_tiles(destination_dir, self.append_log, tiles_x, tiles_y, self.title_le.text(), self.description_le.text())


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
