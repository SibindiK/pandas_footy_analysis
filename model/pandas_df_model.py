from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

class PandasModel(qtc.QAbstractTableModel):

    def __init__(self, df):
        qtc.QAbstractTableModel.__init__(self)
        self.df = df

    def rowCount(self, parent=None):
        return self.df.shape[0]
    
    def columnCount(self, parent=None):
        return self.df.shape[1]
    
    def data(self, index, role=qtc.Qt.DisplayRole):
        if index.isValid():
            if role == qtc.Qt.DisplayRole:
                return str(self.df.iloc[index.row(), index.column()])
        return None
        
    def headerData(self, col, orientation, role):
        if (orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole):
            return self.df.columns[col]
        return None


