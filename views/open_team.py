from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import os


class OpenTeamDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        loadUi(os.path.join('views', 'open_dialog.ui'), self)
        self.connectSignalsSlots()
        self.teamToOpen = ''

    def connectSignalsSlots(self):
        self.buttonBox.accepted.connect(self.accepted_)

    def loadData(self, payload):
        self.listWidget.addItems(payload)

    def accepted_(self):
        teams = self.listWidget.selectedItems()
        if (len(teams)):
            self.teamToOpen = teams[0].text()

    def getTeamName(self):
        return self.teamToOpen

    def open_(self):
        self.exec()
        return QDialog.Accepted
