import sys

#Added sys.path.append to allow importing modules from folder structure 
#See - https://www.youtube.com/watch?v=lR-OKnX7uOw
sys.path.append("..")

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from model.pandas_df_model import PandasModel
from model.analysis_executor import AnalysisExecutor
from model.analysis_goals_scored import AnalysisGoalsScored
from model.analysis_goals_conceded import AnalysisGoalsConceded

from model.league_builder import LeagueBuilder

from view.analysis_selection import Ui_MainWindow

class AnalysisSelector(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, df, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df = df
        self.setupUi(self)
        self.analysis_ui_events_manager()
        
    def analysis_ui_events_manager(self):
        self.closeButton.clicked.connect(self.close)
        self.submitButton.clicked.connect(self.filter_data)
    
    def filter_data(self):
        #create the summariser df based on team type
        df = LeagueBuilder(self.df)
        if (self.teamTypeComboBox.currentText() == 'HomeTeam'):
            if (self.attributeComboBox.currentText() == 'HT Goals Scored'):
                df = df.build_ht_league_table('HomeTeam')
                self.analyser = AnalysisExecutor(AnalysisGoalsScored())
            elif (self.attributeComboBox.currentText() == 'HT Goals Conceded'):
                df = df.build_ht_league_table('HomeTeam')
                self.analyser = AnalysisExecutor(AnalysisGoalsConceded())
            elif (self.attributeComboBox.currentText() == 'FT Goals Scored'):
                df = df.build_ft_league_table('HomeTeam')
                self.analyser = AnalysisExecutor(AnalysisGoalsScored())
            elif (self.attributeComboBox.currentText() == 'FT Goals Conceded'):
                df = df.build_ft_league_table('HomeTeam')
                self.analyser = AnalysisExecutor(AnalysisGoalsConceded())
        elif (self.teamTypeComboBox.currentText() == 'AwayTeam'):
            if (self.attributeComboBox.currentText() == 'HT Goals Scored'):
                df = df.build_ht_league_table('AwayTeam')
                self.analyser = AnalysisExecutor(AnalysisGoalsScored())
            elif (self.attributeComboBox.currentText() == 'HT Goals Conceded'):
                df = df.build_ht_league_table('AwayTeam')
                self.analyser = AnalysisExecutor(AnalysisGoalsConceded())
            elif (self.attributeComboBox.currentText() == 'FT Goals Scored'):
                df = df.build_ft_league_table('AwayTeam')
                self.analyser = AnalysisExecutor(AnalysisGoalsScored())
            elif (self.attributeComboBox.currentText() == 'FT Goals Conceded'):
                df = df.build_ft_league_table('AwayTeam')
                self.analyser = AnalysisExecutor(AnalysisGoalsConceded())

        df = self.analyser.execute_analysis(df, self.compareComboBox.currentText(),
                             self.percentSpinBox.value())
        _analysis_model = PandasModel(df)
        self.analysisTableView.setModel(_analysis_model)

