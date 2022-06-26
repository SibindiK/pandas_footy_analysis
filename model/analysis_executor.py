import pandas as pd

from model.analysis_strategy import AnalysisStrategy

def select_and_sort(df:pd.DataFrame, comparison:str, value:float):
    if (comparison == 'more than'):    
        df = df.loc[df['Ratio%'] >= value,:]
    elif (comparison == 'less than'):
        df = df.loc[df['Ratio%'] <= value,:]
    df = df.sort_values(by='Ratio%', ascending=False)
    return df


class AnalysisExecutor:
    ''' instantiates the analysis strategy of choice'''
    def __init__(self, analysis:AnalysisStrategy):
        self._analysis = analysis
        
    def execute_analysis(self, df:pd.DataFrame, comparison:str, value:float):
        _df = self._analysis.analyse(df)
        _df = select_and_sort(_df, comparison, value)
        return (_df)
