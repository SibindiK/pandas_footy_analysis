import sys

#Added sys.path.append to allow importing modules from folder structure 
#See - https://www.youtube.com/watch?v=lR-OKnX7uOw
sys.path.append("..")

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from model.pandas_df_model import PandasModel
from model.Analyser import Analyser

from view.analysis_selection import Ui_MainWindow

class AnalysisSelector(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, df, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df = df
        self.setupUi(self)
        self.analysis_ui_events_manager()
        
    def analysis_ui_events_manager(self):
        self.closeButton.clicked.connect(self.close)
        self.submitButton.clicked.connect(self.filter_data)
    
    def filter_data(self):
        self.analyser = Analyser(self.df)
        _analysis_df = self.analyser.analysis(self.teamTypeComboBox.currentText(),
                            self.attributeComboBox.currentText(),
                            self.compareComboBox.currentText(),
                            float(self.percentSpinBox.value()))
        _analysis_model = PandasModel(_analysis_df)
        self.analysisTableView.setModel(_analysis_model)

