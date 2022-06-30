import pandas as pd
from model.analysis_strategy import AnalysisStrategy
from model.helper_functions import percentage_ratio

class AnalysisGoalsScored(AnalysisStrategy):
    '''Strategy to return goals scored analysis'''
            
    def analyse(self, df:pd.DataFrame):
        '''perform the analysis'''
        df['Ratio%'] = percentage_ratio(df['GamesScored'], df['Played'])
        df = df.sort_values(by='Ratio%', ascending=False)
        return df
