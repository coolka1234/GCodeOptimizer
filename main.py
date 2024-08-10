from src.gui.main_window import Ui_MainWindow
from src.backend.functions import handle_the_line
from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButtonConfirm.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        file_path = self.lineEditFilePath.text()
        handle_the_line(file_path)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    