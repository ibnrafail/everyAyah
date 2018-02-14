import sys
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.uic import loadUi
import json
from urllib.request import urlretrieve

# 0 problem in line edit


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("everyAyah.ui", self)

        self.surahs = json.load(open("surah.json"))
        self.surahs_by_index = {int(value['index']): key for (key, value) in self.surahs.items()}

        self.setWindowTitle("Every Ayah")

        self.downloadBtn.clicked.connect(self.on_download_btn_clicked)
        self.browseBtn.clicked.connect(self.on_browse_btn_clicked)
        self.surahComboBox.currentIndexChanged.connect(self.on_surah_cmbox_index_changed)

        self.surahComboBox.insertItems(0, self.surahs_by_index.values())
        self.on_surah_cmbox_index_changed()

    @pyqtSlot()
    def on_download_btn_clicked(self):
        from_int = self.spinBoxFrom.value()
        to_int = self.spinBoxTo.value()
        index = self.surahComboBox.currentIndex() + 1

        destination = self.lineEditFilePath.text()

        if not os.path.exists(destination):
            os.makedirs(destination)

        destination += "/"

        for i in range(from_int, to_int + 1):
            url = "http://www.everyayah.com/data/MaherAlMuaiqly128kbps/" + "{0:0>3}".format(i) + "{0:0>3}".format(index) + ".mp3"
            print(url)
            urlretrieve(url, destination + str(i) + "_" + str(index) + ".mp3")

    @pyqtSlot()
    def on_browse_btn_clicked(self):
        self.lineEditFilePath.setText(QFileDialog.getExistingDirectory())

    @pyqtSlot()
    def on_surah_cmbox_index_changed(self):
        from_num = int(self.surahs[self.surahComboBox.currentText()]["juz"][0]["verse"]["start"].split("verse_")[1])
        to_num = int(self.surahs[self.surahComboBox.currentText()]["juz"][-1]["verse"]["end"].split("verse_")[1])

        self.spinBoxFrom.setMaximum(to_num)
        self.spinBoxTo.setMaximum(to_num)

        self.spinBoxFrom.setValue(from_num)
        self.spinBoxTo.setValue(to_num)


app = QApplication(sys.argv)
w = Main()
w.show()
sys.exit(app.exec_())
