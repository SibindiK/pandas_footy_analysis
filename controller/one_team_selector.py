import sys
#Added sys.path.append to allow importing modules from folder structure 
#See - https://www.youtube.com/watch?v=lR-OKnX7uOw
sys.path.append("..")

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from model.pandas_df_model import PandasModel
from model.league_builder import LeagueBuilder

from view.one_team_view_ui import Ui_oneTeamWindow

class OneTeamSelector(qtw.QMainWindow, Ui_oneTeamWindow):
    '''Brings up view for selecting the data of one team'''
    def __init__(self, df, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df = df
        self.setupUi(self)
        self.one_team_events_manager()
        
        
    def one_team_events_manager(self):
        self.submitTeamButton.clicked.connect(self.one_team_data)
        self.quitButton.clicked.connect(self.close)
    
    def one_team_data(self):
        '''filters dfs by one team populates views'''
        _lg_table = LeagueBuilder(self.df)
        _selected_team = self.teamLineEdit.text()
        if (_selected_team):
            #get all home games for one team
            _selected_team_home_model = PandasModel(
                    _lg_table.get_one_team_games_df('HomeTeam', _selected_team))
            self.homeGamesTableView.setModel(_selected_team_home_model)
            #summarise home full time stats
            _homes_ft_league_df = _lg_table.build_ft_league_table('HomeTeam')
            _homes_ft_summary_df = _lg_table.get_one_team_summary('HomeTeam', 
                    _homes_ft_league_df, _selected_team)
            _homes_ft_summary_model = PandasModel(_homes_ft_summary_df)
            self.homeSummaryTableView.setModel(_homes_ft_summary_model)
            #summarise home half time stats
            _homes_ht_league_df = _lg_table.build_ht_league_table('HomeTeam')
            _homes_ht_summary_df = _lg_table.get_one_team_summary('HomeTeam', 
                    _homes_ht_league_df, _selected_team)
            _homes_ht_summary_model = PandasModel(_homes_ht_summary_df)
            self.homeHTSummaryTableView.setModel(_homes_ht_summary_model)
            #get all away games for one team
            _selected_team_away_model = PandasModel(
                    _lg_table.get_one_team_games_df('AwayTeam', _selected_team))
            self.awayGamesTableView.setModel(_selected_team_away_model)
            #summarise away full time stats
            _away_ft_league_df = _lg_table.build_ft_league_table('AwayTeam')
            _away_ft_summary_df = _lg_table.get_one_team_summary('AwayTeam', 
                    _away_ft_league_df, _selected_team)
            _away_ft_summary_model = PandasModel(_away_ft_summary_df)
            self.awaySummaryTableView.setModel(_away_ft_summary_model)
            #summarise away half time stats
            _away_ht_league_df = _lg_table.build_ht_league_table('AwayTeam')
            _away_ht_summary_df = _lg_table.get_one_team_summary('AwayTeam', 
                    _away_ht_league_df, _selected_team)
            _away_ht_summary_model = PandasModel(_away_ht_summary_df)
            self.awayHTSummaryTableView.setModel(_away_ht_summary_model)

