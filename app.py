"""
Fantasy Cricket App

Created By : Gaurav Maddesia 

Date : 19/04/2022

"""

import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QAction, QMainWindow, QLabel, QMessageBox, QPushButton)
from views.main_window import Ui_MainWindow

from views.new_team import NewTeamDialog
from views.open_team import OpenTeamDialog
from views.eval_team import EvalTeamDialog
from model.model import GameDataModel

MIN_PLAYERS = 8
NUM_MATCHES = 1


class Window (QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.msgBox = QMessageBox(parent=self)
        self.connectSignalsSlots()
        self.gdm = GameDataModel()
        self.currTeam = ""
        self.teamPoints = 0
        self.preloadData()

    def connectSignalsSlots(self):
        self.actionNEW_Team.triggered.connect(self.newTeamAction)
        self.actionOPEN_TEam.triggered.connect(self.openTeamAction)
        self.actionEVALUTE_Team.triggered.connect(self.evalTeamAction)
        self.actionSAVE_Team.triggered.connect(self.saveTeamAction)
        self.radio_bat.toggled.connect(
            lambda: self.radioToggled(self.radio_bat))
        self.radio_bow.toggled.connect(
            lambda: self.radioToggled(self.radio_bow))
        self.radio_ar.toggled.connect(lambda: self.radioToggled(self.radio_ar))
        self.radio_wk.toggled.connect(lambda: self.radioToggled(self.radio_wk))
        self.listWidget_nonSlPlayers.itemDoubleClicked.connect(
            lambda: self.playerSelected())

    def preloadData(self):
        self.bats = self.gdm.getPlayers("BAT")
        self.bwls = self.gdm.getPlayers("BWL")
        self.wks = self.gdm.getPlayers("WK")
        self.ars = self.gdm.getPlayers("AR")
        self.teams = self.gdm.getTeams()
        self.matches = []
        for i in range(NUM_MATCHES):
            self.matches.append(self.gdm.getMatch(i+1))

    def addCurrentTeam(self):
        if self.currTeam != "" and len(self.selectedPlayers) > MIN_PLAYERS:
            for team in self.teams:
                if (team["name"] == self.currTeam):
                    return True
            self.teams.append({"name": self.currTeam, "players": [
                player for player in self.selectedPlayers], "value": 0})
            return True
        else:
            self.showMsgBox("Insuffient Data to Evalute !!")
            return False

    def teamExists(self):
        for team in self.teams:
            if (team["name"] == self.currTeam):
                if (team["value"] == self.teamPoints):
                    temp = self.selectedPlayers.copy()
                    for p in team["players"]:
                        if p in temp:
                            temp.pop(p)
                    if len(temp) == 0:
                        return True
        return False

    def saveTeamAction(self):
        if self.teamPoints:
            players = [player for player in self.selectedPlayers]
            if not self.teamExists():
                self.gdm.addTeam(
                    self.currTeam, players, self.teamPoints)
                self.showMsgBox("Saved Successfully!!",
                                QMessageBox.Information, "Success")
                for team in self.teams:
                    if team["name"] == self.currTeam:
                        team["value"] = self.teamPoints
            else:
                self.showMsgBox("Team Already Exists!!",
                                QMessageBox.Information, "Info")

        else:
            if self.currTeam == "":
                self.showMsgBox("Open or Create a team first!!",
                                QMessageBox.Critical, "Error")
            else:
                self.showMsgBox("Please evaluate your team first!!",
                                QMessageBox.Warning, "Warning")

    def evalTeamAction(self):
        if self.currTeam == "":
            self.showMsgBox("Open or Create a team first!!",
                            QMessageBox.Critical, "Error")
            return
        if (self.addCurrentTeam()):
            dialog = EvalTeamDialog(self)
            dialog.loadData(self.currTeam, self.teams, self.matches)
            dialog.setModal(True)
            res = dialog.open_()
            if res == QDialog.Accepted:
                self.teamPoints = dialog.getTotalPoints()

    def openTeamAction(self):
        dialog = OpenTeamDialog(self)
        dialog.setModal(True)
        dialog.loadData([team["name"] for team in self.teams])
        result = dialog.open_()
        if (result == QDialog.Accepted):
            temp = dialog.getTeamName()
            if temp != '':
                self.currTeam = temp
                self.openTeam()

    def openTeam(self):
        team = self.gdm.getTeams(self.currTeam)
        self.selectedPlayers = {}
        self.listWidget_slPlayers.clear()
        self.listWidget_nonSlPlayers.clear()
        self.teamPoints = 0
        self.lblState = [0, 0, 0, 0, 1000, 0, self.currTeam]
        self.notSelected_bats = self.bats.copy()
        self.notSelected_bwls = self.bwls.copy()
        self.notSelected_wks = self.wks.copy()
        self.notSelected_ars = self.ars.copy()
        for player in team["players"]:
            if player in self.notSelected_bats:
                self.updateSelections(
                    0, self.notSelected_bats[player], player, self.notSelected_bats)
            elif player in self.notSelected_bwls:
                self.updateSelections(
                    1, self.notSelected_bwls[player], player, self.notSelected_bwls)
            elif player in self.notSelected_wks:
                self.updateSelections(
                    2, self.notSelected_wks[player], player, self.notSelected_wks)
            else:
                self.updateSelections(
                    3, self.notSelected_ars[player], player, self.notSelected_ars)
        for player in self.selectedPlayers:
            self.updateTeam(player)
        self.updateLabels()
        self.radio_bat.setChecked(True)

    def newTeamAction(self):
        dialog = NewTeamDialog(self)
        dialog.setModal(True)
        dialog.loadOldData([team["name"] for team in self.teams])
        result = dialog.open_()
        if (result == QDialog.Accepted):
            temp = dialog.getTeamName()
        if (temp != ""):
            self.currTeam = temp
            self.teamPoints = 0
            self.lblState = [0, 0, 0, 0, 1000, 0, self.currTeam]
            self.updateLabels()
            self.notSelected_bats = self.bats.copy()
            self.notSelected_bwls = self.bwls.copy()
            self.notSelected_wks = self.wks.copy()
            self.notSelected_ars = self.ars.copy()
            self.selectedPlayers = {}
            self.listWidget_slPlayers.clear()
            self.radio_bat.setChecked(True)

    def radioToggled(self, b):
        if b.isChecked() and self.currTeam != "":
            type = b.text()
            self.listWidget_nonSlPlayers.clear()
            if (type == 'BAT'):
                self.listWidget_nonSlPlayers.addItems(self.notSelected_bats)
            elif (type == "BWL"):
                self.listWidget_nonSlPlayers.addItems(self.notSelected_bwls)
            elif (type == "WK"):
                self.listWidget_nonSlPlayers.addItems(self.notSelected_wks)
            else:
                self.listWidget_nonSlPlayers.addItems(self.notSelected_ars)

    def validatePlayerSel(self, value, type, playersList):
        msg = f"You can\'t add any more {type}!!"
        if (len(playersList) < 2 or (self.lblState[4]-value < 0)):
            self.showMsgBox(msg)
            return False
        return True

    def playerSelected(self):
        player = self.listWidget_nonSlPlayers.selectedItems()[0].text()
        if player in self.notSelected_bats:
            value = self.notSelected_bats[player]
            if self.validatePlayerSel(value, 'batsmen', self.notSelected_bats):
                self.listWidget_nonSlPlayers.clear()
                self.updateSelections(0, value, player, self.notSelected_bats)
                self.listWidget_nonSlPlayers.addItems(self.notSelected_bats)
            else:
                return
        elif player in self.notSelected_bwls:
            value = self.notSelected_bwls[player]
            if self.validatePlayerSel(value, 'bowler', self.notSelected_bwls):
                self.listWidget_nonSlPlayers.clear()
                self.updateSelections(1, value, player, self.notSelected_bwls)
                self.listWidget_nonSlPlayers.addItems(self.notSelected_bwls)
            else:
                return
        elif player in self.notSelected_wks:
            value = self.notSelected_wks[player]
            if self.validatePlayerSel(value, 'wicket-keeper', self.notSelected_wks):
                self.listWidget_nonSlPlayers.clear()
                self.updateSelections(2, value, player, self.notSelected_wks)
                self.listWidget_nonSlPlayers.addItems(self.notSelected_wks)
            else:
                return
        else:
            value = self.notSelected_ars[player]
            if self.validatePlayerSel(value, 'all-rounders', self.notSelected_ars):
                self.listWidget_nonSlPlayers.clear()
                self.updateSelections(3, value, player, self.notSelected_ars)
                self.listWidget_nonSlPlayers.addItems(self.notSelected_ars)
            else:
                return
        self.updateTeam(player)
        self.updateLabels()

    def updateSelections(self, l, value, player, playersList):
        self.lblState[l] += 1
        self.lblState[4] -= value
        self.lblState[5] += value
        self.selectedPlayers[player] = value
        playersList.pop(player)

    def updateTeam(self, player):
        self.listWidget_slPlayers.addItem(player)

    def updateLabels(self):
        self.batCount.setText(str(self.lblState[0]))
        self.bowCount.setText(str(self.lblState[1]))
        self.wkCount.setText(str(self.lblState[2]))
        self.arCount.setText(str(self.lblState[3]))
        self.avPoints.setText(str(self.lblState[4]))
        self.usedPoints.setText(str(self.lblState[5]))
        self.team_name.setText(self.lblState[6])

    def showMsgBox(self, msg, icon=QMessageBox.Critical, title="Error"):
        self.msgBox.setIcon(icon)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setInformativeText(msg)
        self.msgBox.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
