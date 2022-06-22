import sys
#Added sys.path.append to allow importing modules from folder structure 
#See - https://www.youtube.com/watch?v=lR-OKnX7uOw
sys.path.append("..")

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from view.dialog_leagues_selector import Ui_AllLeaguesDialog

class SelectedLeague(qtw.QDialog, Ui_AllLeaguesDialog):
    league_selected_signal = qtc.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.league = ' '

        self.listWidget.itemClicked.connect(self.set_league)
        self.listWidget.itemClicked.connect(self.update_league_label)
        self.cancelButton.clicked.connect(self.close)

    def set_league(self):
        lge = self.listWidget.currentItem().text()
        if (lge == "Premier League"):
            self.league = 'E0'
        elif (lge == "Championship"):
            self.league = 'E1'
        elif (lge == "League One"):
            self.league = 'E2'
        elif (lge == "League Two"):
            self.league = 'E3'
        elif (lge == "National League"):
            self.league = 'EC'
        elif (lge == "Premiership"):
            self.league = 'SC0'
        elif (lge == "Championship SC"):
            self.league = 'SC1'
        elif (lge == "League One SC"):
            self.league = 'SC2'
        elif (lge == "League Two SC"):
            self.league = 'SC3'
        elif (lge == "Bundesliga"):
            self.league = 'D1'
        elif (lge == "Bundesliga Two"):
            self.league = 'D2'
        elif (lge == "La Liga"):
            self.league = 'SP1'
        elif (lge == "La Liga Two"):
            self.league = 'SP2'
        elif (lge == "Serie A"):
            self.league = 'I1'
        elif (lge == "Serie B"):
            self.league = 'I2'
        elif (lge == "Ligue One"):
            self.league = 'F1'
        elif (lge == "Ligue Two"):
            self.league = 'F2'
        elif (lge == "Belgium Jupiler Pro League"):
            self.league = 'B1'
        elif (lge == "Netherlands Eredivisie"):
            self.league = 'N1'
        elif (lge == "Portugal Primeira Liga"):
            self.league = 'P1'
        elif (lge == "Turkey Super Lig"):
            self.league = 'T1'
        elif (lge == "Greece Super League"):
            self.league = 'G1'
        self.league_selected_signal.emit(self.league)
        

    #updates the league label as user moves down the leagues list
    def update_league_label(self):
        self.leagueLabel.setText(self.listWidget.currentItem().text())

        
        
        

