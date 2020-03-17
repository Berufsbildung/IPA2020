import opti
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = opti.Ui_opti()
    ui.setupUi(MainWindow)
    ui.combobox_setup()
    ui.choice()
    app.quit
    MainWindow.show()
    sys.exit(app.exec_())


# import first_ui
# 
# 
# if __name__ == "__main__":
#     import sys
#     app = first_ui.QtWidgets.QApplication(sys.argv)
#     MainWindow = first_ui.QtWidgets.QMainWindow()
#     ui = first_ui.Ui_temperature()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())