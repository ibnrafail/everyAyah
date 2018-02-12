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
        super(Main, self).__init__()
        loadUi("everyAyah.ui", self)

        self.to_str = ""
        self.from_str = ""
        self.lineEditStyle = self.lineEditFrom.styleSheet()
        self.surahs = json.load(open("surah.json"))
        self.surahs_by_index = {int(value['index']): key for (key, value) in self.surahs.items()}



        self.setWindowTitle("Every Ayah")

        self.downloadBtn.clicked.connect(self.on_download_btn_clicked)
        self.browseBtn.clicked.connect(self.on_browse_btn_clicked)
        self.surahComboBox.currentIndexChanged.connect(self.on_surah_cmbox_index_changed)
        self.lineEditFrom.editingFinished.connect(self.on_from_line_edit_edit_finish)
        self.lineEditFrom.textEdited.connect(self.on_from_line_edit_text_edited)
        self.lineEditTo.textEdited.connect(self.on_to_line_edit_text_edited)

        self.surahComboBox.insertItems(0, self.surahs_by_index.values())
        self.on_surah_cmbox_index_changed()

    @pyqtSlot()
    def on_download_btn_clicked(self):
        from_line = int(self.lineEditFrom.text())
        to_line = int(self.lineEditTo.text())

        if from_line == 0:
            self.lineEditFrom.setStyleSheet("border: 1px solid red;")

        if to_line == 0:
            self.lineEditTo.setStyleSheet("border: 1px solid red;")

        if from_line != 0 and to_line != 0:
            self.lineEditFilePath.setText(str(from_line) + " " + str(to_line))

    @pyqtSlot()
    def on_browse_btn_clicked(self):
        self.lineEditFilePath.setText(QFileDialog.getExistingDirectory())

    @pyqtSlot()
    def on_surah_cmbox_index_changed(self):
        self.from_str = self.surahs[self.surahComboBox.currentText()]["juz"][0]["verse"]["start"].split("verse_")[1]
        self.to_str = self.surahs[self.surahComboBox.currentText()]["juz"][-1]["verse"]["end"].split("verse_")[1]
        from_num = int(self.from_str)
        to_num = int(self.to_str)
        self.lineEditFrom.setText(self.from_str)
        self.lineEditTo.setText(self.to_str)
        self.lineEditFrom.setValidator(QIntValidator(from_num, to_num, self))
        self.lineEditTo.setValidator(QIntValidator(from_num, to_num, self))

    @pyqtSlot()
    def on_from_line_edit_edit_finish(self):
        print(self.lineEditFrom.text())
        if int(self.lineEditFrom.text()) == 0 or int(self.lineEditFrom.text()) > int(self.lineEditTo.text()):
            self.lineEditFrom.setText(self.from_str)

    @pyqtSlot()
    def on_from_line_edit_text_edited(self):
        self.lineEditFrom.setStyleSheet(self.lineEditStyle)

    @pyqtSlot()
    def on_to_line_edit_text_edited(self):
        self.lineEditTo.setStyleSheet(self.lineEditStyle)

app = QApplication(sys.argv)
w = Main()
w.show()
sys.exit(app.exec_())
