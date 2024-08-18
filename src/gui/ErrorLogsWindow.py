from src.gui.error_logs_window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow
class ErrorLogsWindows(Ui_MainWindow, QMainWindow):
    def __init__(self, logs):
        super().__init__()
        self.setupUi(self)
        self.listWidget.addItems(logs)