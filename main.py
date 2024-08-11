import os
from src.gui.main_window import Ui_MainWindow
from src.backend.functions import get_and_write as main
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from src.backend.local_logging import logger
import logging

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
        if not file_path.endswith('.nc'):
            QMessageBox.critical(self, 'Error', 'The file is not a .nc file')
        if not os.path.exists(file_path):
            QMessageBox.critical(self, 'Error', 'The file does not exist')
        if not os.path.exists(save_path):
            QMessageBox.critical(self, 'Error', 'The save path does not exist')
        if save_path == '':
            save_path = file_path.replace('.nc', '_processed.nc')
        else:
            save_path = save_path + '/' + file_path.split('/')[-1].replace('.nc', '_processed.nc')
        main(file_path, save_path) 

    def initialize_log_combobox(self):
        self.comboBoxLoggingLevel.addItem('DEBUG')
        self.comboBoxLoggingLevel.addItem('INFO')
        self.comboBoxLoggingLevel.addItem('WARNING')
        self.comboBoxLoggingLevel.addItem('ERROR')
        self.comboBoxLoggingLevel.addItem('CRITICAL')
        self.comboBoxLoggingLevel.setCurrentText('DEBUG')
    
    def set_logging_level(self):
        logging_level = self.comboBoxLoggingLevel.currentText()
        if logging_level == 'DEBUG':
            logger.setLevel(logging.DEBUG)
        elif logging_level == 'INFO':
            logger.setLevel(logging.INFO)
        elif logging_level == 'WARNING':
            logger.setLevel(logging.WARNING)
        elif logging_level == 'ERROR':
            logger.setLevel(logging.ERROR)
        elif logging_level == 'CRITICAL':
            logger.setLevel(logging.CRITICAL)
        logger.info(f"Logging level set to {logging_level}")
    
    def initialize_language_combobox(self):
        self.comboBoxLanguage.addItem('English')
        self.comboBoxLanguage.addItem('Polish')
        self.comboBoxLanguage.setCurrentText('English')
    
    def set_language(self):
        language = self.comboBoxLanguage.currentText()
        if language == 'English':
            self.pushButtonChooseFile.setText('Choose file')
            self.pushButtonChooseSave.setText('Choose save path')
            self.pushButtonConfirm.setText('Confirm')
            self.lineEditFilePath.setPlaceholderText('File to process...')
            self.lineEditSavePath.setPlaceholderText('Save location...')
            self.labelLoggingLevel.setText('Select logging level:')
            self.labelLanguage.setText('Select language:')
        elif language == 'Polish':
            self.pushButtonChooseFile.setText('Wybierz plik')
            self.pushButtonChooseSave.setText('Wybierz ścieżkę zapisu')
            self.pushButtonConfirm.setText('Potwierdź')
            self.lineEditFilePath.setPlaceholderText('Plik do przetworzenia...')
            self.lineEditSavePath.setPlaceholderText('Lokalizacja zapisu...')
            self.labelLoggingLevel.setText('Wybierz poziom logowania:')
            self.labelLanguage.setText('Wybierz język:')
        logger.info(f"Language set to {language}")


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
