from src.gui.main_window import Ui_MainWindow
from src.backend.optimize_gcode import main
from PyQt6.QtWidgets import QMainWindow, QFileDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButtonChooseFile.clicked.connect(self.open_file)
        self.pushButtonChooseSave.clicked.connect(self.choose_save_path)
        
   
    def open_file(self):
        self.lineEditFilePath.setText(QFileDialog.getOpenFileName(self, 'Open file', '')[0])
    
    def choose_save_path(self):
        self.lineEditSavePath.setText(QFileDialog.getExistingDirectory(self, 'Choose save path'))
    
    def execute(self):
        main(self.lineEditFilePath.text(), self.lineEditSavePath.text()) 



if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    