from PyQt5.QtWidgets import QDialog, QPushButton, QMessageBox
from PyQt5.uic import loadUi
import os


class NewTeamDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        loadUi(os.path.join('views', 'new_team.ui'), self)
        self.msgBox = QMessageBox(parent=self)
        self.createBtn = self.findChild(QPushButton, "create_team_btn")
        self.createBtn.setEnabled(False)
        self.newTeam = ''
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.lineEdit_createTeamName.textChanged.connect(self.textUpdated)
        self.createBtn.clicked.connect(self.createAction)

    def loadOldData(self, oldNames):
        self.oldNames = oldNames

    def textUpdated(self, text):
        if len(text) > 0:
            self.createBtn.setEnabled(True)
        else:
            self.createBtn.setEnabled(False)

    def createAction(self):
        self.newTeam = self.lineEdit_createTeamName.text()
        if self.newTeam in self.oldNames:
            self.msgBox.setIcon(QMessageBox.Critical)
            self.msgBox.setWindowTitle("Error")
            self.msgBox.setInformativeText("Name already exists")
            self.msgBox.exec_()
            self.newTeam = ""
            return
        self.reject()

    def getTeamName(self):
        return self.newTeam

    def open_(self):
        self.exec()
        return QDialog.Accepted
