import pandas as pd

from model.summariser import Summariser
#Calculate percentage
percentage_ratio = lambda x, y : round((x/y) * 100, 2)

#FUTURE WORK - Redesign class to separate some functions 
# Does class currently violate single responsibility principle?
#KS - 21 June 2022
class Analyser(Summariser):
    '''
    -creates the various analysis columns from the primary df
    -filters rows and columns to return items of interest
    _builds league tables
    '''
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.df = super().get_summary_df()

#Add won draw and lost columns
    def insert_won_draw_lost_columns(self, df, won, draw, lost):
        df.insert(2, 'Won', won)
        df.insert(3, 'Draw', draw)
        df.insert(4, 'Lost', lost)
#Add scored columns        
    def insert_scored_columns(self, df, scored, scored2, no_score):
        df.insert(5, 'GamesScored', scored)
        df.insert(6, 'Scored2', scored2)
        df.insert(7, 'FailToScore', no_score)

#Add goals conceded columns
    def insert_goals_conceded_columns(self, df, conceded):
        df['GamesConceded'] = conceded

#Change NA's to zeros and apply round 
    def prettify_table(self, _df, team_type:str):
        #remove the team names column as these are strings
        team_col = _df.pop(team_type)
        _df = _df.fillna(0).applymap(round)
        _df.insert(0, team_type, team_col) #return team names 
        return _df

#Filter df by the various attributes selected by user    
    def analysis(self, team_type:str, attribute:str, comparison:str, value:float):
        _df = self.sum_up_table(team_type)
        #User interested in Half time home goals scored 
        if (attribute == 'HT Goals Scored'):
            attribute = 'HTHG'
            self.insert_won_draw_lost_columns(_df, self.home_ht_won, 
                    self.home_ht_draw, self.home_ht_lost)
            self.insert_scored_columns(_df, self.home_ht_scored, 
                    self.home_ht_scored2, self.home_ht_no_score)
            #Select only columns of interest
            _df = _df[[team_type,'Played','Won','Draw','Lost','GamesScored',
                    'Scored2','FailToScore',attribute,'HTAG','HomeHTPts']]
            _df['Ratio%'] = percentage_ratio(_df['GamesScored'], _df['Played'])
        #User interested in Half time home goals conceded
        elif(attribute == 'HT Goals Conceded'):
            attribute = 'HTAG'
            self.insert_won_draw_lost_columns(_df, self.home_ht_won, 
                    self.home_ht_draw, self.home_ht_lost)
            self.insert_scored_columns(_df, self.home_ht_scored, 
                    self.home_ht_scored2, self.home_ht_no_score)
            self.insert_goals_conceded_columns(_df,self.home_ht_conceded)
            #Select only columns of interest
            _df = _df[[team_type,'Played','Won','Draw','Lost','GamesConceded',
                    attribute,'GamesScored','HTHG','HomeHTPts']]
            _df['Ratio%'] = percentage_ratio(_df['GamesConceded'], _df['Played'])
        #User interested in Full time home goals scored
        elif(attribute == 'FT Goals Scored'):
            attribute = 'FTHG'
        elif (attribute == 'FT Goals Conceded'):
            attribute = 'FTAG'
        
        if (comparison == 'more than'):    
            _df = _df.loc[_df['Ratio%'] >= value,:]
        elif (comparison == 'less than'):
            _df = _df.loc[_df['Ratio%'] <= value,:]
        _df = self.prettify_table(_df, team_type)
        _df = _df.sort_values(by='Ratio%', ascending=False)
        return _df

#Pivot the data table by team type i.e hometeam or away team and get sum of attributes    
    def sum_up_table(self, team_type:str):
        games_played = self.df[team_type].value_counts() #get number of games played
        _df = pd.pivot_table(self.df, index=[team_type], aggfunc = 'sum')
        _df[team_type] = _df.index
        _df.insert(1, 'Played',games_played)
        team_col = _df.pop(team_type)
        _df.insert(0, team_type, team_col)
        return _df

#Build fulltime league tables
    def build_ft_league_table(self, team_type:str):
        _df = self.sum_up_table(team_type)
        #Homes Fulltime table 
        if (team_type == 'HomeTeam'):
                self.insert_won_draw_lost_columns(_df, self.home_won, 
                    self.home_draw, self.home_lost)
                self.insert_scored_columns(_df, self.home_scored, 
                    self.home_scored2, self.home_no_score)
                self.insert_goals_conceded_columns(_df,self.home_conceded)
                #Select only columns of interest
                _df = _df[[team_type,'Played','Won','Draw','Lost','HomePts',
                        'GamesScored','Scored2','FTHG','FailToScore',
                        'GamesConceded','HS','HST','HC','HY','HR']]
                _df = _df.sort_values(by='HomePts', ascending=False)
        #Aways Fulltime table
        elif (team_type == 'AwayTeam'):
                self.insert_won_draw_lost_columns(_df, self.away_won, 
                    self.away_draw, self.away_lost)
                self.insert_scored_columns(_df, self.away_scored, 
                    self.away_scored2, self.away_no_score)
                self.insert_goals_conceded_columns(_df,self.away_conceded)
                #Select only columns of interest
                _df = _df[[team_type,'Played','Won','Draw','Lost','AwayPts',
                        'GamesScored','Scored2','FTAG','FailToScore',
                        'GamesConceded','AS','AST','AC','AY','AR']]
                _df = _df.sort_values(by='AwayPts', ascending=False)
        _df = self.prettify_table(_df, team_type)
        return _df

#Build halftime league tables
    def build_ht_league_table(self, team_type:str):
        _df = self.sum_up_table(team_type)
        #Homes Halftime table
        if (team_type == 'HomeTeam'):
                self.insert_won_draw_lost_columns(_df, self.home_ht_won, 
                    self.home_ht_draw, self.home_ht_lost)
                self.insert_scored_columns(_df, self.home_ht_scored, 
                    self.home_ht_scored2, self.home_ht_no_score)
                self.insert_goals_conceded_columns(_df,self.home_ht_conceded)
                #Select only columns of interest
                _df = _df[[team_type,'Played','Won','Draw','Lost','HomeHTPts',
                        'GamesScored','Scored2','HTHG','FailToScore',
                        'GamesConceded']]
                _df = _df.sort_values(by='HomeHTPts', ascending=False)
        #Aways Halftime table
        elif (team_type == 'AwayTeam'):
                self.insert_won_draw_lost_columns(_df, self.away_ht_won, 
                    self.away_ht_draw, self.away_ht_lost)
                self.insert_scored_columns(_df, self.away_ht_scored, 
                    self.away_ht_scored2, self.away_ht_no_score)
                self.insert_goals_conceded_columns(_df,self.away_ht_conceded)
                #Select only columns of interest
                _df = _df[[team_type,'Played','Won','Draw','Lost','AwayHTPts',
                        'GamesScored','Scored2','HTAG','FailToScore',
                        'GamesConceded']]
                _df = _df.sort_values(by='AwayHTPts', ascending=False)
        _df = self.prettify_table(_df, team_type)
        return _df
                    
#Combine homes and aways tables to build full time table 
    def combine_homes_and_away_league_table(self, game_type:str):
        #param game_type - checks if we're interested in full time or half time stats  
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

#Build scored 1+ analysis
    def build_scored_analyis(self, game_type:str, goals:int):
        _df = self.combine_homes_and_away_league_table(game_type)
        _df['Scored1+%'] = percentage_ratio(_df['GamesScored'], _df['Played'])
        _df['Scored2+%'] = percentage_ratio(_df['Scored2'], _df['Played'])
        _df = _df[['Team','Played','GamesScored','Scored1+%','Scored2',
                'Scored2+%','GoalsScored','FailToScore','GamesConceded']]
        _df = self.prettify_table(_df, 'Team')
        if (goals == 1):        
                _df = _df.sort_values(by='Scored1+%', ascending=False)
        elif (goals == 2):        
                _df = _df.sort_values(by='Scored2+%', ascending=False)
        return _df
