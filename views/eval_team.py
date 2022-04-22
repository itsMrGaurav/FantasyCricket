from PyQt5.QtWidgets import QDialog, QComboBox, QPushButton, QLabel
from PyQt5.uic import loadUi
from sqlalchemy import false
import os


class EvalTeamDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        loadUi(os.path.join('views', 'eval_dialog.ui'), self)
        self.comboSelTeam = self.findChild(QComboBox, "combo_select_team")
        self.comboSelMatch = self.findChild(QComboBox, "combo_select_match")
        self.currPlayers = []
        self.currMatch = []
        self.totalPoints = 0
        self.newTeam = ""
        self.calculate_btn = self.findChild(QPushButton, "push_calculate_btn")
        self.totalLabel = self.findChild(QLabel, "eval_points")
        self.calculate_btn.setEnabled(False)
        self.connectSignalsSlots()

    def loadData(self, currTeam, teams, matches):
        self.teams = teams
        self.newTeam = currTeam
        self.matches = matches
        self.comboSelTeam.addItems(team["name"] for team in teams)
        self.comboSelMatch.addItems(
            f"Match {i+1}" for i in range(len(matches)))

    def connectSignalsSlots(self):
        self.comboSelTeam.activated.connect(self.teamUpdated)
        self.comboSelMatch.activated.connect(self.matchUpdated)
        self.calculate_btn.clicked.connect(self.calculatePoints)

    def teamUpdated(self, id):
        currTeam = self.comboSelTeam.currentText()
        self.listWidget_Players.clear()
        self.listWidget_Points.clear()
        self.totalLabel.setText("####")
        if currTeam == 'Select Team':
            self.currPlayers = []
            self.calculate_btn.setEnabled(False)
            return
        for team in self.teams:
            if team["name"] == currTeam:
                self.populateWithPlayers(team["players"])
                self.currPlayers = team["players"]
        if (len(self.currMatch) > 0):
            self.calculate_btn.setEnabled(True)
        else:
            self.calculate_btn.setEnabled(False)
            self.totalLabel.setText("####")

    def matchUpdated(self, id):
        match = self.comboSelMatch.currentText()
        if match == 'Select Match':
            self.currMatch = []
            self.listWidget_Points.clear()
            self.calculate_btn.setEnabled(False)
            self.totalLabel.setText("####")
            return
        id = int(match.split(" ")[1])
        self.currMatch = self.matches[id-1]
        if (len(self.currPlayers) > 0):
            self.calculate_btn.setEnabled(True)
        else:
            self.calculate_btn.setEnabled(False)
            self.totalLabel.setText("####")

    def populateWithPlayers(self, players):
        self.listWidget_Players.clear()
        self.listWidget_Players.addItems(players)

    def calculatePoints(self):
        self.listWidget_Points.clear()
        self.totalPoints = 0
        for player in self.currPlayers:
            for playerData in self.currMatch:
                if playerData["name"] == player:
                    points = self.getPoints(playerData)
                    self.listWidget_Points.addItem(str(points))
                    self.totalPoints += points
        self.totalLabel.setText(str(self.totalPoints))

    def getTotalPoints(self):
        if self.comboSelTeam.currentText() == self.newTeam:
            return self.totalPoints
        else:
            return 0

    def getPoints(self, player):
        runs = player["scored"]
        points = runs/2  # 1 for 2 runs
        if runs > 99:
            points += 10
        elif runs > 49:
            points += 5
        sr = 0
        if player['faced']:
            sr = runs * 1.0 / player["faced"]  # strike rate
        if sr > 100:
            points += 4
        elif sr > 80:
            points += 2
        points += player['fours']
        points += player['sixes'] * 2
        wkts = player['wkts']
        points += wkts * 10
        if wkts >= 5:
            points += 10
        elif wkts >= 3:
            points += 5
        er = 0
        if player["bowled"]:
            er = player['given'] * 1.0 / \
                (player['bowled'] / 6.0)   # economy rate
        if er < 2:
            points += 10
        elif er > 2 and er < 3.5:
            points += 7
        elif er > 3.5 and er < 4.5:
            points += 4
        points += 10 * player['catches']
        points += 10 * player['stumping']
        points += 10 * player['ro']
        return int(points)

    def open_(self):
        self.exec()
        return QDialog.Accepted
