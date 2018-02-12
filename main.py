import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator
import json
from pprint import pprint

# 0 problem in line edit

class Main(QWidget):
    def __init__(self):
        self.surahs = json.load(open("surah.json"))
        self.surahs_by_index = {int(value['index']): key for (key, value) in self.surahs.items()}

        super(Main, self).__init__()
        loadUi("everyAyah.ui", self)

        self.setWindowTitle("Every Ayah")

        self.downloadBtn.clicked.connect(self.on_download_btn_clicked)
        self.browseBtn.clicked.connect(self.on_browse_btn_clicked)
        self.surahComboBox.currentIndexChanged.connect(self.on_surah_cmbox_index_changed)

        self.surahComboBox.insertItems(0, self.surahs_by_index.values())
        self.on_surah_cmbox_index_changed()

    @pyqtSlot()
    def on_download_btn_clicked(self):
        from_line = self.lineEditFrom.text()
        to_line = self.lineEditTo.text()

        self.lineEditFilePath.setText("Text")

    @pyqtSlot()
    def on_browse_btn_clicked(self):
        self.lineEditFilePath.setText(QFileDialog.getExistingDirectory())

    @pyqtSlot()
    def on_surah_cmbox_index_changed(self):
        from_str = self.surahs[self.surahComboBox.currentText()]["juz"][0]["verse"]["start"].split("verse_")[1]
        to_str = self.surahs[self.surahComboBox.currentText()]["juz"][-1]["verse"]["end"].split("verse_")[1]
        from_num = int(from_str)
        to_num = int(to_str)
        self.lineEditFrom.setText(from_str)
        self.lineEditTo.setText(to_str)
        self.lineEditFrom.setValidator(QIntValidator(from_num, to_num, self))
        self.lineEditTo.setValidator(QIntValidator(from_num, to_num, self))


app = QApplication(sys.argv)
w = Main()
w.show()
sys.exit(app.exec_())
