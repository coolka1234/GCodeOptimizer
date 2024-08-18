from src.gui.logs_window import Ui_Logs
from PyQt6.QtWidgets import QMainWindow
class LogsWindows(Ui_Logs):
    def __init__(self, logs):
        self.setupUi(self)
        self.listWidget.addItems(logs)