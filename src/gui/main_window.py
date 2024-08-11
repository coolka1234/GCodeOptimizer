# Form implementation generated from reading ui file 'src/gui/main_window.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(929, 533)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(11, 11, 911, 501))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEditFilePath = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEditFilePath.setText("")
        self.lineEditFilePath.setObjectName("lineEditFilePath")
        self.horizontalLayout_3.addWidget(self.lineEditFilePath)
        self.lineEditSavePath = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEditSavePath.setText("")
        self.lineEditSavePath.setObjectName("lineEditSavePath")
        self.horizontalLayout_3.addWidget(self.lineEditSavePath)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButtonChooseFile = QtWidgets.QPushButton(parent=self.widget)
        self.pushButtonChooseFile.setObjectName("pushButtonChooseFile")
        self.horizontalLayout_2.addWidget(self.pushButtonChooseFile)
        self.pushButtonChooseSave = QtWidgets.QPushButton(parent=self.widget)
        self.pushButtonChooseSave.setObjectName("pushButtonChooseSave")
        self.horizontalLayout_2.addWidget(self.pushButtonChooseSave)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelLanguage = QtWidgets.QLabel(parent=self.widget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        self.labelLanguage.setFont(font)
        self.labelLanguage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLanguage.setObjectName("labelLanguage")
        self.horizontalLayout.addWidget(self.labelLanguage)
        self.labelLoggingLevel = QtWidgets.QLabel(parent=self.widget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        self.labelLoggingLevel.setFont(font)
        self.labelLoggingLevel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLoggingLevel.setObjectName("labelLoggingLevel")
        self.horizontalLayout.addWidget(self.labelLoggingLevel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.comboBoxLanguage = QtWidgets.QComboBox(parent=self.widget)
        self.comboBoxLanguage.setEditable(False)
        self.comboBoxLanguage.setCurrentText("")
        self.comboBoxLanguage.setObjectName("comboBoxLanguage")
        self.horizontalLayout_4.addWidget(self.comboBoxLanguage)
        self.comboBoxLoggingLevel = QtWidgets.QComboBox(parent=self.widget)
        self.comboBoxLoggingLevel.setObjectName("comboBoxLoggingLevel")
        self.horizontalLayout_4.addWidget(self.comboBoxLoggingLevel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButtonConfirm = QtWidgets.QPushButton(parent=self.widget)
        self.pushButtonConfirm.setObjectName("pushButtonConfirm")
        self.verticalLayout.addWidget(self.pushButtonConfirm)
        self.progressBar = QtWidgets.QProgressBar(parent=self.widget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GCode Optimizer"))
        self.lineEditFilePath.setPlaceholderText(_translate("MainWindow", "File to process..."))
        self.lineEditSavePath.setPlaceholderText(_translate("MainWindow", "Save location..."))
        self.pushButtonChooseFile.setText(_translate("MainWindow", "Choose file..."))
        self.pushButtonChooseSave.setText(_translate("MainWindow", "Choose save location..."))
        self.labelLanguage.setText(_translate("MainWindow", "Select language"))
        self.labelLoggingLevel.setText(_translate("MainWindow", "Select logging level"))
        self.comboBoxLanguage.setPlaceholderText(_translate("MainWindow", "Language..."))
        self.comboBoxLoggingLevel.setPlaceholderText(_translate("MainWindow", "Logging level..."))
        self.pushButtonConfirm.setText(_translate("MainWindow", "Confirm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
