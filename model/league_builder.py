import pandas as pd

from model import constants as cc
from model.summariser import Summariser
from model.helper_functions import percentage_ratio

class LeagueBuilder(Summariser):
    '''
    -creates the various analysis columns from the primary df
    -filters rows and columns to return items of interest
    _builds league tables
    '''
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.df = super().get_summary_df()

    def build_ft_league_table(self, team_type:str):
        '''Build fulltime league tables'''
        _df = super().sum_up_table(team_type)
        #Homes Fulltime table 
        if (team_type == 'HomeTeam'):
                super().insert_won_draw_lost_columns(_df, self.home_won, 
                    self.home_draw, self.home_lost)
                super().insert_scored_columns(_df, self.home_scored, 
                    self.home_scored2, self.home_no_score)
                super().insert_goals_conceded_columns(_df,self.home_conceded)
                #Select only columns of interest
                cc.FT_HOMES_TABLE_DATA_COLS.insert(0, team_type)
                _df = _df[cc.FT_HOMES_TABLE_DATA_COLS]
                _df = _df.sort_values(by='HomePts', ascending=False)
        #Aways Fulltime table
        elif (team_type == 'AwayTeam'):
                super().insert_won_draw_lost_columns(_df, self.away_won, 
                    self.away_draw, self.away_lost)
                super().insert_scored_columns(_df, self.away_scored, 
                    self.away_scored2, self.away_no_score)
                super().insert_goals_conceded_columns(_df,self.away_conceded)
                #Select only columns of interest
                cc.FT_AWAYS_TABLE_DATA_COLS.insert(0, team_type)
                _df = _df[cc.FT_AWAYS_TABLE_DATA_COLS]
                _df = _df.sort_values(by='AwayPts', ascending=False)
        _df = super().prettify_table(_df, team_type)
        return _df

    def build_ht_league_table(self, team_type:str):
        '''Build halftime league tables'''
        _df = super().sum_up_table(team_type)
        #Homes Halftime table
        if (team_type == 'HomeTeam'):
                super().insert_won_draw_lost_columns(_df, self.home_ht_won, 
                    self.home_ht_draw, self.home_ht_lost)
                super().insert_scored_columns(_df, self.home_ht_scored, 
                    self.home_ht_scored2, self.home_ht_no_score)
                super().insert_goals_conceded_columns(_df,self.home_ht_conceded)
                #Select only columns of interest
                cc.HT_HOMES_TABLE_DATA_COLS.insert(0, team_type)
                _df = _df[cc.HT_HOMES_TABLE_DATA_COLS]
                _df = _df.sort_values(by='HomeHTPts', ascending=False)
        #Aways Halftime table
        elif (team_type == 'AwayTeam'):
                super().insert_won_draw_lost_columns(_df, self.away_ht_won, 
                    self.away_ht_draw, self.away_ht_lost)
                super().insert_scored_columns(_df, self.away_ht_scored, 
                    self.away_ht_scored2, self.away_ht_no_score)
                super().insert_goals_conceded_columns(_df,self.away_ht_conceded)
                #Select only columns of interest
                cc.HT_AWAYS_TABLE_DATA_COLS.insert(0, team_type)
                _df = _df[cc.HT_AWAYS_TABLE_DATA_COLS]
                _df = _df.sort_values(by='AwayHTPts', ascending=False)
        _df = super().prettify_table(_df, team_type)
        return _df
                    
    def combine_homes_and_away_league_table(self, game_type:str):
        '''Combine homes and aways tables to build full league table 
           param game_type - checks if we're interested in full time or half time stats  
        '''
        if (game_type == 'FT'):
                _homes_df = self.build_ft_league_table('HomeTeam')
                _homes_df =_homes_df.rename(columns={'HomePts':'Points', 
                        'FTHG':'GoalsScored', 'HS':'Shots',
                        'HST':'ShotsTarget','HC':'Corners',
                        'HY':'Yellow','HR':'Red'})
                _away_df = self.build_ft_league_table('AwayTeam')
                _away_df = _away_df.rename(columns={'AwayPts':'Points', 
                        'FTAG':'GoalsScored', 'AS':'Shots',
                        'AST':'ShotsTarget','AC':'Corners',
                        'AY':'Yellow','AR':'Red'})
        elif (game_type == 'HT'):
                _homes_df = self.build_ht_league_table('HomeTeam')
                _homes_df = _homes_df.rename(columns={'HomeHTPts':'Points', 
                        'HTHG':'GoalsScored'})
                _away_df = self.build_ht_league_table('AwayTeam')
                _away_df = _away_df.rename(columns={'AwayHTPts':'Points', 
                        'HTAG':'GoalsScored'})
        _homes_df = _homes_df.rename(columns={'HomeTeam':'Team'})
        _away_df = _away_df.rename(columns={'AwayTeam':'Team'})        
        _df = pd.concat([_homes_df, _away_df]).groupby(['Team']).sum().reset_index()
        _df = _df.sort_values(by='Points', ascending=False)
        return _df

    def build_scored_analyis(self, game_type:str, goals:int):
        '''Build scored 1+ analysis'''
        _df = self.combine_homes_and_away_league_table(game_type)
        _df['Scored1+%'] = percentage_ratio(_df['GamesScored'], _df['Played'])
        _df['Scored2+%'] = percentage_ratio(_df['Scored2'], _df['Played'])
        _df = _df[['Team','Played','GamesScored','Scored1+%','Scored2',
                'Scored2+%','GoalsScored','FailToScore','GamesConceded']]
        _df = super().prettify_table(_df, 'Team')
        if (goals == 1):        
                _df = _df.sort_values(by='Scored1+%', ascending=False)
        elif (goals == 2):        
                _df = _df.sort_values(by='Scored2+%', ascending=False)
        return _df

    def get_one_team_games_df(self, team_type:str, team:str):
        '''Filter df to get the home or awaygames for one particular team'''
        _df = self.df.loc[self.df[team_type] == team,]
        return _df

    def get_one_team_summary(self, team_type:str, df:pd.DataFrame, team:str):
        '''#Filter league table to get summary for only one team'''
        _df = df.loc[df[team_type] == team]
        return _df
