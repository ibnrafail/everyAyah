import sys
import os
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.uic import loadUi
import json
from urllib.request import urlretrieve
from collections import OrderedDict


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("everyAyah.ui", self)
        self.surahs = json.load(open("surah.json"))
        self.surahs_by_index = OrderedDict(
            sorted({int(value['index']): key for (key, value) in self.surahs.items()}.items()))
        self.setWindowTitle("Every Ayah")

        self.downloadBtn.clicked.connect(self.on_download_btn_clicked)
        self.browseBtn.clicked.connect(self.on_browse_btn_clicked)
        self.surahComboBox.currentIndexChanged.connect(self.on_surah_cmbox_index_changed)
        self.spinBoxTo.valueChanged.connect(self.on_spin_box_to_value_changed)
        self.spinBoxFrom.valueChanged.connect(self.on_spin_box_from_value_changed)

        self.surahComboBox.insertItems(1, self.surahs_by_index.values())
        self.on_surah_cmbox_index_changed()
        self.spinBoxToPreviousValue = self.spinBoxTo.value()
        self.spinBoxFromPreviousValue = self.spinBoxFrom.value()

        self.reciters = {"Abu Bakr Al-Shatri": "Abu_Bakr_Ash-Shaatree_128kbps",
                         "Maher Al-Muaiqly": "MaherAlMuaiqly128kbps",
                         "Mishary Rashid Alafasy": "Alafasy_128kbps"}
        self.reciterComboBox.insertItems(1, self.reciters.keys())
        self.reset_progress()

    @pyqtSlot()
    def on_download_btn_clicked(self):
        self.progressBar.setValue(0.0)
        from_int = self.spinBoxFrom.value()
        to_int = self.spinBoxTo.value()
        index = self.surahComboBox.currentIndex() + 1
        reciter = self.reciters[self.reciterComboBox.currentText()]
        destination = self.lineEditFilePath.text()

        if not os.path.exists(destination):
            try:
                os.makedirs(destination)
            except FileNotFoundError:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Invalid path set")
                msg.setWindowTitle("Error")
                msg.show()
            return

        destination += "/"
        self.progress_label.setText(str(0) + "/" + str(to_int))
        for i in range(from_int, to_int + 1):
            url = "http://www.everyayah.com/data/" + reciter + "/" + \
                  "{0:0>3}".format(index) + "{0:0>3}".format(i) + ".mp3"
            print(url)
            urlretrieve(url, destination + str(index) + "_" + str(i) + ".mp3")
            self.progressBar.setValue((float(i) / float(to_int)) * 100.0)
            self.progress_label.setText(str(i) + "/" + str(to_int))

    @pyqtSlot()
    def on_browse_btn_clicked(self):
        self.lineEditFilePath.setText(QFileDialog.getExistingDirectory())
        self.reset_progress()

    @pyqtSlot()
    def on_surah_cmbox_index_changed(self):
        from_num = int(self.surahs[self.surahComboBox.currentText()]["juz"][0]["verse"]["start"].split("verse_")[1])
        to_num = int(self.surahs[self.surahComboBox.currentText()]["juz"][-1]["verse"]["end"].split("verse_")[1])

        self.spinBoxFrom.setMaximum(to_num)
        self.spinBoxTo.setMaximum(to_num)

        self.spinBoxFrom.setValue(from_num)
        self.spinBoxTo.setValue(to_num)
        self.reset_progress()
    
    @pyqtSlot()
    def on_spin_box_to_value_changed(self):
        if self.spinBoxTo.value() < self.spinBoxFrom.value():
            self.spinBoxTo.setValue(self.spinBoxToPreviousValue)
        else:
            self.spinBoxToPreviousValue = self.spinBoxTo.value()
        self.reset_progress()
    
    @pyqtSlot()
    def on_spin_box_from_value_changed(self):
        if self.spinBoxTo.value() < self.spinBoxFrom.value():
            self.spinBoxFrom.setValue(self.spinBoxFromPreviousValue)
        else:
            self.spinBoxFromPreviousValue = self.spinBoxFrom.value()

        self.reset_progress()

    def reset_progress(self):
        self.progressBar.setValue(0)
        self.progress_label.setText("")


app = QApplication(sys.argv)
w = Main()
w.show()
sys.exit(app.exec_())
