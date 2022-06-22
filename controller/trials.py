import sys
#Added sys.path.append to allow importing modules from folder structure 
#See - https://www.youtube.com/watch?v=lR-OKnX7uOw
sys.path.append("..")

from PyQt5 import QtWidgets
from model import data_import as di
from view.selector_view import Ui_MainWindow

class Controller():
    def __init__(self):
        self.main_ui = Ui_MainWindow()

    def events_manager(self):    
        self.main_ui.loadAllLeaguesButton.clicked.connect(di.main)

def print_hello():
    print("Hello Kermit")
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    controller = Controller()
    controller.main_ui.setupUi(MainWindow)
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    MainWindow.show()
    controller.events_manager()
    sys.exit(app.exec_())