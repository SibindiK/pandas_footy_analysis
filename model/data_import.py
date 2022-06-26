import pandas as pd
from model import constants as cc

class FootyData():
    '''
    class to load football data from source site into pandas dataframes.
    main_leagues_df : holds data for all available leagues
    one_league_df : holds data for one league as chosen by user
    latest_fixtures : dataframe to hold latest fixtures
    '''
    def __init__(self, data_url:str, fixtures_url:str):
        self.data_url = data_url
        self.fixtures_url = fixtures_url
        #empty data frame used to clear views
        self.empty_df = pd.DataFrame()

#Load dataframe for one league only i.e. df from one sheet
#Note use of lambda function to ensure cases where the column is not found
#do not throw errors; missing cols loaded as NaNs (sheet_name = EC has missing cols)
    def set_one_league_df(self, sname:str):
        self.one_league_df = pd.read_excel(self.data_url, 
                sheet_name=sname, usecols=lambda c: c in set(cc.MAIN_LEAGUES_DATA_COLS))
        

#Load data frame for all leagues i.e. df from all sheets    
    def set_main_leagues_df(self):
        self.main_leagues_df = pd.concat(pd.read_excel(self.data_url, 
                sheet_name=None, usecols=lambda c: c in set(cc.MAIN_LEAGUES_DATA_COLS)),
                ignore_index=True)

#Load other leagues        
    def set_other_league_df(self, path:str):
        self.one_league_df = pd.read_excel(path, 
                sheet_name=None, usecols=lambda c: c in set(cc.OTHER_LEAGUES_DATA_COLS))

#Load latest fixtures for all leagues
    def set_latest_fixtures(self):
        self.latest_fixtures = pd.read_excel(self.fixtures_url, 
                    sheet_name='fixtures', usecols=lambda c: c in set(cc.FIXTURES_DATA_COLS))

#Filter fixtures df to get specific league        
    def set_specific_league_fixtures(self, league:str):
        _specific_league_fixtures = self.latest_fixtures.loc[self.latest_fixtures['Div']==league]
        return _specific_league_fixtures

