from src.gui.main_window import Ui_MainWindow
from src.backend.functions import get_and_write as main
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButtonChooseFile.clicked.connect(self.open_file)
        self.pushButtonChooseSave.clicked.connect(self.choose_save_path)
        self.pushButtonConfirm.clicked.connect(self.execute)
        
   
    def open_file(self):
        self.lineEditFilePath.setText(QFileDialog.getOpenFileName()[0])
    
    def choose_save_path(self):
        self.lineEditSavePath.setText(QFileDialog.getExistingDirectory(self, 'Choose save path'))
    
    def execute(self):
        save_path= self.lineEditSavePath.text()
        file_path= self.lineEditFilePath.text()
        if file_path == '':
            QMessageBox.critical(self, 'Error', 'Please choose a file')
        if save_path == '':
            save_path = file_path.replace('.nc', '_processed.nc')
        else:
            save_path = save_path + '/' + file_path.split('/')[-1].replace('.nc', '_processed.nc')
        main(file_path, save_path) 



if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
