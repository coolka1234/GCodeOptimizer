# This file contains the main window of the application
from main_window import Ui_MainWindow
from PyQt6 import QtWidgets
from backend.functions import handle_the_line

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonConfirm.clicked.connect(self.on_pushButtonConfirm_clicked)

    def on_pushButtonConfirm_clicked(self):
        print("Button clicked")