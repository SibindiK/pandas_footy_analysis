import sys

#Added sys.path.append to allow importing modules from folder structure 
#See - https://www.youtube.com/watch?v=lR-OKnX7uOw
sys.path.append("..")

import pandas as pd
import webbrowser

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from controller.analysis_selector import AnalysisSelector
from controller.league_selector import SelectedLeague
from controller.one_team_selector import OneTeamSelector 

from model import constants as cc
from model.data_import import FootyData
from model.excel_files import MyExcelFile
from model.league_builder import LeagueBuilder
from model.pandas_df_model import PandasModel

from view.main_view  import Ui_MainWindow



class MainController(qtw.QMainWindow, Ui_MainWindow):
    ''' '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.f_data = FootyData(cc.ALL_EURO_LEAGUES_DATA_URL, cc.ALL_EURO_FIXTURES_URL)
        self.excel_file = MyExcelFile(cc.EXCEL_FILE_PATH)
        self.selected_league = SelectedLeague()
        self.primary_df = pd.DataFrame()
        self.main_ui_events_manager()


    def main_ui_events_manager(self):
        #data loading menu item events        
        self.main_ui.actionAll_Main_Leagues.triggered.connect(
            self.load_main_leagues)
        self.main_ui.actionSpecific_League.triggered.connect(
            self.selected_league.show)
        self.main_ui.actionFootball_data_Website.triggered.connect(
            lambda: self.open_website(cc.MAIN_FOOTBALL_DATA_WEBSITE_URL))
        #leagues menus
        self.main_ui.actionLeague_Table.triggered.connect(
            lambda: self.combined_league_table('FT'))
        self.main_ui.actionHomes_Table.triggered.connect(
            lambda: self.display_ft_league_table('HomeTeam'))
        self.main_ui.actionAways_Table.triggered.connect(
            lambda: self.display_ft_league_table('AwayTeam'))    
        self.main_ui.actionHalf_Time_Table.triggered.connect(
            lambda: self.combined_league_table('HT'))
        self.main_ui.actionHT_Homes_Table.triggered.connect(
            lambda: self.display_ht_league_table('HomeTeam'))
        self.main_ui.actionHT_Aways_Table.triggered.connect(
            lambda: self.display_ht_league_table('AwayTeam'))    
        #scored menus
        self.main_ui.actionFT_1_Scored.triggered.connect(
            lambda: self.games_scored('FT', 1))
        self.main_ui.actionFT_2_Scored.triggered.connect(
            lambda: self.games_scored('FT', 2))
        self.main_ui.actionHT_1_Scored.triggered.connect(
            lambda: self.games_scored('HT', 1))
        self.main_ui.actionHT_2_Scored.triggered.connect(
            lambda: self.games_scored('HT', 2))
        #conceded menus
        self.main_ui.actionFT_1_Conceded.triggered.connect(
            lambda: self.games_conceded('FT', 1))
        self.main_ui.actionFT_2_Conceded.triggered.connect(
            lambda: self.games_conceded('FT', 2))
        self.main_ui.actionHT_1_Conceded.triggered.connect(
            lambda: self.games_conceded('HT', 1))
        self.main_ui.actionHT_2_Conceded.triggered.connect(
            lambda: self.games_conceded('HT', 2))

        #home and away scored menus
        self.main_ui.actionWrite_to_Excel.triggered.connect(
            self.export_to_excel)
        self.main_ui.actionSelection.triggered.connect(
            self.start_analysis)
        self.main_ui.menuExit.triggered.connect(self.close)
        self.main_ui.actionOne_Team_Data.triggered.connect(
            self.display_one_team)
# league selector ui events
        self.selected_league.selectButton.clicked.connect(self.load_specific_league)

#Check if dataframe has any elements
    def df_is_empty(self, df:pd.DataFrame):
        if (df.size <= 0):
            return True
        else:
            return False

#Load data for all leagues  
    def load_main_leagues(self):
        self.main_ui.statusLabel.setText(cc.LOADING_IN_PROGRESS_MESSAGE)
        self.f_data.set_main_leagues_df()
        self.f_data.set_latest_fixtures()
        self.view_active_data_frame(self.f_data.main_leagues_df, self.f_data.latest_fixtures)
        self.primary_df = self.f_data.main_leagues_df
        self.main_ui.statusLabel.setText(cc.LOADING_COMPLETE_MESSAGE)

#Load a specific league from the available selection
    def load_specific_league(self):
        self.f_data.set_one_league_df(self.selected_league.league)
        self.f_data.set_latest_fixtures()
        _lg_fix_df = self.f_data.set_specific_league_fixtures(self.selected_league.league)
        if (_lg_fix_df.size > 0):
            self.view_active_data_frame(self.f_data.one_league_df, _lg_fix_df)
        else:
            self.view_active_data_frame(self.f_data.one_league_df, self.f_data.empty_df)
        self.primary_df = self.f_data.one_league_df
        self.selected_league.close()
        self.main_ui.statusLabel.setText(f"{self.selected_league.leagueLabel.text()}" +
                cc.LOADING_COMPLETE_MESSAGE)
        
#Update the main view area with the games dataframe and fixtures dataframe.
    def view_active_data_frame(self, *args:pd.DataFrame):
        _games_df_data_model = PandasModel(args[0])
        self.main_ui.mainTableView.setModel(_games_df_data_model)
        if (len(args) > 1):
            _fixtures_df_data_model = PandasModel(args[1])
            self.main_ui.fixturesTableView.setModel(_fixtures_df_data_model)

#Bring up analysis view to enable user to set parameter selections 
    def start_analysis(self):
        if (self.df_is_empty(self.primary_df)):
            self.main_ui.statusLabel.setText(cc.NO_DATA_MESSAGE)
        else:
            self.selected_analysis = AnalysisSelector(self.primary_df)
            self.selected_analysis.show()

#Bring up Ui for user to select only one team
    def display_one_team(self):
        if (self.df_is_empty(self.primary_df)):
            self.main_ui.statusLabel.setText(cc.NO_DATA_MESSAGE)
        else:
            self.selected_team = OneTeamSelector(self.primary_df)
            self.selected_team.show()

#display full time home or away league table
    def display_ft_league_table(self, type:str):
        if (self.df_is_empty(self.primary_df)):
            self.main_ui.statusLabel.setText(cc.NO_DATA_MESSAGE)
        else:
            _ft_league = LeagueBuilder(self.primary_df)
            self.view_active_data_frame(_ft_league.build_ft_league_table(type))

#display half time home or away league table
    def display_ht_league_table(self, type:str):
        if (self.df_is_empty(self.primary_df)):
            self.main_ui.statusLabel.setText(cc.NO_DATA_MESSAGE)
        else:
            _ht_league = LeagueBuilder(self.primary_df)
            self.view_active_data_frame(_ht_league.build_ht_league_table(type))

#display league table that shows totals of all games, home and away
    def combined_league_table(self, type:str):
        if (self.df_is_empty(self.primary_df)):
            self.main_ui.statusLabel.setText(cc.NO_DATA_MESSAGE)
        else:
            _league = LeagueBuilder(self.primary_df)
            self.view_active_data_frame(_league.combine_homes_and_away_league_table(type))

#display data for goals scored
    def games_scored(self, type:str, goals:int):
        if (self.df_is_empty(self.primary_df)):
            self.main_ui.statusLabel.setText(cc.NO_DATA_MESSAGE)
        else:
            _scored = LeagueBuilder(self.primary_df)
            self.view_active_data_frame(_scored.build_scored_table(type, goals))

#display data for goals scored
    def games_conceded(self, type:str, goals:int):
        if (self.df_is_empty(self.primary_df)):
            self.main_ui.statusLabel.setText(cc.NO_DATA_MESSAGE)
        else:
            _conceded = LeagueBuilder(self.primary_df)
            self.view_active_data_frame(_conceded.build_conceded_table(type, goals))

#Write data to excel
    def export_to_excel(self):
        self.excel_file.write_df_to_excel_file(self.f_data.main_leagues_df)        

#Open default web browser at specified site
    def open_website(self, site_url:str):
        webbrowser.open_new(site_url)
