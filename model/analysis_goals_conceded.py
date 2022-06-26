import pandas as pd
from model.analysis_strategy import AnalysisStrategy
from model.helper_functions import percentage_ratio

class AnalysisGoalsConceded(AnalysisStrategy):
    '''Strategy to return goals scored analysis'''
            
    def analyse(self, df:pd.DataFrame):
        '''perform the analysis'''
        df['Ratio%'] = percentage_ratio(df['GamesConceded'], df['Played'])
        return df
