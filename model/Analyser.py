import pandas as pd

from model.summariser import Summariser
from model.summariser import percentage_ratio

class Analyser(Summariser):
    '''
    -filters rows and columns to return stats of interest eg return all
    teams which have scored a goal by half time in 50% of their home games
    -returns data for only one team 
    '''
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.df = super().get_summary_df()

#Filter df by the various attributes selected by user    
    def analysis(self, team_type:str, attribute:str, comparison:str, value:float):
        _df = super().sum_up_table(team_type)
        #User interested in Half time home goals scored 
        if (attribute == 'HT Goals Scored'):
            attribute = 'HTHG'
            super().insert_won_draw_lost_columns(_df, self.home_ht_won, 
                    self.home_ht_draw, self.home_ht_lost)
            super().insert_scored_columns(_df, self.home_ht_scored, 
                    self.home_ht_scored2, self.home_ht_no_score)
            #Select only columns of interest
            _df = _df[[team_type,'Played','Won','Draw','Lost','GamesScored',
                    'Scored2','FailToScore',attribute,'HTAG','HomeHTPts']]
            _df['Ratio%'] = percentage_ratio(_df['GamesScored'], _df['Played'])
        #User interested in Half time home goals conceded
        elif(attribute == 'HT Goals Conceded'):
            attribute = 'HTAG'
            super().insert_won_draw_lost_columns(_df, self.home_ht_won, 
                    self.home_ht_draw, self.home_ht_lost)
            super().insert_scored_columns(_df, self.home_ht_scored, 
                    self.home_ht_scored2, self.home_ht_no_score)
            super().insert_goals_conceded_columns(_df,self.home_ht_conceded)
            #Select only columns of interest
            _df = _df[[team_type,'Played','Won','Draw','Lost','GamesConceded',
                    attribute,'GamesScored','HTHG','HomeHTPts']]
            _df['Ratio%'] = percentage_ratio(_df['GamesConceded'], _df['Played'])
        #User interested in Full time home goals scored
        elif(attribute == 'FT Goals Scored'):
            attribute = 'FTHG'
            super().insert_won_draw_lost_columns(_df, self.home_won, 
                    self.home_draw, self.home_lost)
            super().insert_scored_columns(_df, self.home_scored, 
                    self.home_scored2, self.home_no_score)
            #Select only columns of interest
            _df = _df[[team_type,'Played','Won','Draw','Lost','GamesScored',
                    'Scored2','FailToScore',attribute,'FTHG','HomePts']]
            _df['Ratio%'] = percentage_ratio(_df['GamesScored'], _df['Played'])

        elif (attribute == 'FT Goals Conceded'):
            attribute = 'FTAG'
        
        if (comparison == 'more than'):    
            _df = _df.loc[_df['Ratio%'] >= value,:]
        elif (comparison == 'less than'):
            _df = _df.loc[_df['Ratio%'] <= value,:]
        _df = super().prettify_table(_df, team_type)
        _df = _df.sort_values(by='Ratio%', ascending=False)
        return _df

#Filter df to get the home games for one particular team
    def get_one_team_homes_df(self, team:str):
        _homes_df = self.df.loc[self.df.HomeTeam == team,]
        return _homes_df
    
#Filter df to get the away games for one particular team
    def get_one_team_aways_df(self, team:str):
        _aways_df = self.df.loc[self.df.AwayTeam == team,]
        return _aways_df

#Filter league table to get summary for only one team
    def get_one_team_summary(self, team_type:str, df:pd.DataFrame, team:str):
        _df = df.loc[df[team_type] == team]
        return _df

