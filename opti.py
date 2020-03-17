import first_ui
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_opti(first_ui.Ui_temperature):
    
    def choice(self):
        self.comboBox_1.currentTextChanged.connect(self.setlabel)

    def setlabel(self):
        print(self.comboBox_1.currentText())
        self.checkBox_1.setStyleSheet('background-color: yellow')
        
    def combobox_setup(self):
        colorr = ["Red", "Light Red", "Dark Red", "Orange", "Light Orange", "Dark Orange", "Green", "Light Green", "Dark Green", "Olive",
          "Cyan", "Blue", "Light Blue", "Dark Blue", "Purple", "Magenta", "Pink", "Brown" , "Grey" , "Black"]
        for i in range(20):
            self.comboBox_1.addItem(colorr[i])
            self.comboBox_2.addItem(colorr[i])
            self.comboBox_3.addItem(colorr[i])
            self.comboBox_4.addItem(colorr[i])
            self.comboBox_5.addItem(colorr[i])
            self.comboBox_6.addItem(colorr[i])
            self.comboBox_7.addItem(colorr[i])
            self.comboBox_8.addItem(colorr[i])
            self.comboBox_9.addItem(colorr[i])
            self.comboBox_10.addItem(colorr[i])
            self.comboBox_11.addItem(colorr[i])
            self.comboBox_12.addItem(colorr[i])
            self.comboBox_13.addItem(colorr[i])
            self.comboBox_14.addItem(colorr[i])
            self.comboBox_15.addItem(colorr[i])
            self.comboBox_16.addItem(colorr[i])
            self.comboBox_17.addItem(colorr[i])
            self.comboBox_18.addItem(colorr[i])
            self.comboBox_19.addItem(colorr[i])
            self.comboBox_20.addItem(colorr[i])


# app = QtWidgets.QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# ui = Ui_opti()
#ui.setupUi(MainWindow)
# app.quit


# app = first_ui.QtWidgets.QApplication(sys.argv)
# MainWindow = first_ui.QtWidgets.QMainWindow()
# ui = first_ui.Ui_temperature()
# ui.setupUi(MainWindow)
# app.quit



#ui.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat) 
#ui.comboBox_1.setCurrentIndex(ui.comboBox_1.findText("Pink"))