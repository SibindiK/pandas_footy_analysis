import pandas as pd

class AnalysisStrategy:
    '''Abstract class to define the interface of Analysis strategies'''
    def __init__(self):
        pass
        
    def analyse(self, df:pd.DataFrame):
        '''perform the analysis'''
        pass

