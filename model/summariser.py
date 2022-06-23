import pandas as pd

class Summariser():
    '''
    -creates the various analysis columns from the primary df
    '''
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.create_analysis_and_sum_columns()

    def get_summary_df(self):
        return self.df
        
    def create_analysis_and_sum_columns(self):
#convert 'H','D','A' results to points
        self.df['HomePts'] = self.df['FTR'].map({'H':3, 'A':0, 'D':1})
        self.df['AwayPts'] = self.df['FTR'].map({'H':0, 'A':3, 'D':1})
        self.df['HomeHTPts'] = self.df['HTR'].map({'H':3, 'A':0, 'D':1})
        self.df['AwayHTPts'] = self.df['HTR'].map({'H':0, 'A':3, 'D':1})              
#Home full time and half time wins
        self.home_won = self.df.loc[self.df['FTR']=='H']
        self.home_won = self.home_won['HomeTeam'].value_counts()
        self.home_ht_won = self.df.loc[self.df['HTR']=='H']
        self.home_ht_won = self.home_ht_won['HomeTeam'].value_counts()
#Home full time and half time draws
        self.home_draw = self.df.loc[self.df['FTR']=='D']
        self.home_draw = self.home_draw['HomeTeam'].value_counts()
        self.home_ht_draw = self.df.loc[self.df['HTR']=='D']
        self.home_ht_draw = self.home_ht_draw['HomeTeam'].value_counts()
#Home full time and half time loss
        self.home_lost = self.df.loc[self.df['FTR']=='A']
        self.home_lost = self.home_lost['HomeTeam'].value_counts()
        self.home_ht_lost = self.df.loc[self.df['HTR']=='A']
        self.home_ht_lost = self.home_ht_lost['HomeTeam'].value_counts()
#Home full time and half time failed to score
        self.home_no_score = self.df.loc[self.df['FTHG'] == 0]
        self.home_no_score = self.home_no_score['HomeTeam'].value_counts()
        self.home_ht_no_score = self.df.loc[self.df['HTHG'] == 0]
        self.home_ht_no_score = self.home_ht_no_score['HomeTeam'].value_counts()
#Home full time and half time scored 1+
        self.home_scored = self.df.loc[self.df['FTHG'] > 0]
        self.home_scored = self.home_scored['HomeTeam'].value_counts()
        self.home_ht_scored = self.df.loc[self.df['HTHG'] > 0]
        self.home_ht_scored = self.home_ht_scored['HomeTeam'].value_counts()
#Home full time and half time scored 2+
        self.home_scored2 = self.df.loc[self.df['FTHG'] > 1]
        self.home_scored2 = self.home_scored2['HomeTeam'].value_counts()
        self.home_ht_scored2 = self.df.loc[self.df['HTHG'] > 1]
        self.home_ht_scored2 = self.home_ht_scored2['HomeTeam'].value_counts()
#Home full time and half time clean sheet
        self.home_clean_sheet = self.df.loc[self.df['FTAG'] == 0]
        self.home_clean_sheet = self.home_clean_sheet['HomeTeam'].value_counts()
        self.home_ht_clean_sheet = self.df.loc[self.df['HTAG'] == 0]
        self.home_ht_clean_sheet = self.home_ht_clean_sheet['HomeTeam'].value_counts()
#Home full time and half time conceded
        self.home_conceded = self.df.loc[self.df['FTAG'] > 0]
        self.home_conceded = self.home_conceded['HomeTeam'].value_counts()
        self.home_ht_conceded = self.df.loc[self.df['HTAG'] > 0]
        self.home_ht_conceded = self.home_ht_conceded['HomeTeam'].value_counts()

#Away full time and half time wins
        self.away_won = self.df.loc[self.df['FTR']=='A']
        self.away_won = self.away_won['AwayTeam'].value_counts()
        self.away_ht_won = self.df.loc[self.df['HTR']=='A']
        self.away_ht_won = self.away_ht_won['AwayTeam'].value_counts()
#Away full time and half time draws
        self.away_draw = self.df.loc[self.df['FTR']=='D']
        self.away_draw = self.away_draw['AwayTeam'].value_counts()
        self.away_ht_draw = self.df.loc[self.df['HTR']=='D']
        self.away_ht_draw = self.away_ht_draw['AwayTeam'].value_counts()
#Away full time and half time loss
        self.away_lost = self.df.loc[self.df['FTR']=='H']
        self.away_lost = self.away_lost['AwayTeam'].value_counts()
        self.away_ht_lost = self.df.loc[self.df['HTR']=='H']
        self.away_ht_lost = self.away_ht_lost['AwayTeam'].value_counts()
#Away full time and half time failed to score
        self.away_no_score = self.df.loc[self.df['FTAG'] == 0]
        self.away_no_score = self.away_no_score['AwayTeam'].value_counts()
        self.away_ht_no_score = self.df.loc[self.df['HTAG'] == 0]
        self.away_ht_no_score = self.away_ht_no_score['AwayTeam'].value_counts()
#Away full time and half time scored 1+
        self.away_scored = self.df.loc[self.df['FTAG'] > 0]
        self.away_scored = self.away_scored['AwayTeam'].value_counts()
        self.away_ht_scored = self.df.loc[self.df['HTAG'] > 0]
        self.away_ht_scored = self.away_ht_scored['AwayTeam'].value_counts()
#Away full time and half time scored 2+
        self.away_scored2 = self.df.loc[self.df['FTAG'] > 1]
        self.away_scored2 = self.away_scored2['AwayTeam'].value_counts()
        self.away_ht_scored2 = self.df.loc[self.df['HTAG'] > 1]
        self.away_ht_scored2 = self.away_ht_scored2['AwayTeam'].value_counts()
#Away full time and half time clean sheet
        self.away_clean_sheet = self.df.loc[self.df['FTHG'] == 0]
        self.away_clean_sheet = self.away_clean_sheet['AwayTeam'].value_counts()
        self.away_ht_clean_sheet = self.df.loc[self.df['HTHG'] == 0]
        self.away_ht_clean_sheet = self.away_ht_clean_sheet['AwayTeam'].value_counts()
#Away full time and half time conceded
        self.away_conceded = self.df.loc[self.df['FTHG'] > 0]
        self.away_conceded = self.away_conceded['AwayTeam'].value_counts()
        self.away_ht_conceded = self.df.loc[self.df['HTHG'] > 0]
        self.away_ht_conceded = self.away_ht_conceded['AwayTeam'].value_counts()
