import sys
#Added sys.path.append to allow importing modules from folder structure 
#See - https://www.youtube.com/watch?v=lR-OKnX7uOw
sys.path.append("..")


from PyQt5 import QtWidgets as qtw

from controller.main_controller import MainController

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    
    controller = MainController()
    controller.show()
    
    sys.exit(app.exec_())
