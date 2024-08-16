import os
import traceback
from src.backend import global_vars
from src.gui.main_window import Ui_MainWindow
from src.backend.functions import get_and_write as main
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QSettings
from src.backend.local_logging import logger
import logging

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButtonChooseFile.clicked.connect(self.open_file)
        self.pushButtonChooseSave.clicked.connect(self.choose_save_path)
        self.pushButtonConfirm.clicked.connect(self.execute)
        self.comboBoxLoggingLevel.currentIndexChanged.connect(self.set_logging_level)
        self.comboBoxLanguage.currentIndexChanged.connect(self.set_language)
        self.initialize_log_combobox()
        self.initialize_language_combobox()
        self.settings=QSettings('settings.ini', QSettings.Format.IniFormat)
        self.resize(self.settings.value('size', self.size()))
        self.move(self.settings.value('pos', self.pos()))
        
   
    def open_file(self):
        self.lineEditFilePath.setText(QFileDialog.getOpenFileName()[0])
    
    def choose_save_path(self):
        self.lineEditSavePath.setText(QFileDialog.getExistingDirectory(self, 'Choose save path'))
    
    def execute(self):
        save_path= self.lineEditSavePath.text()
        file_path= self.lineEditFilePath.text()
        if file_path == '':
            QMessageBox.critical(self, 'Error', 'Please choose a file')
            logger.error('No file chosen')
            return
        if not file_path.endswith('.nc'):
            QMessageBox.critical(self, 'Error', 'The file is not a .nc file')
            logger.error('File is not a .nc file')
            return
        if not os.path.exists(file_path):
            QMessageBox.critical(self, 'Error', 'The file does not exist')
            logger.error('File does not exist')
            return
        if not os.path.exists(save_path):
            QMessageBox.critical(self, 'Error', 'The save path does not exist')
            logger.error('Save path does not exist')
            return
        if save_path == '':
            save_path = file_path.replace('.nc', '_processed.nc')
            logger.warning(f"Save path not provided, saving to {save_path}")
        else:
            
            save_path = save_path + '/' + file_path.split('/')[-1].replace('.nc', '_processed.nc')
        try:
            main(file_path, save_path, self.progressBar) 
            QMessageBox.information(self, 'Success', 'File processed successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', 'Error processing file')
            logger.error(f'Error processing file: {e}, traceback: {traceback.format_exc()}')
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
            logger.debug(f"Logging level set to {logging_level}")
        elif logging_level == 'INFO':
            logger.setLevel(logging.INFO)
            logger.info(f"Logging level set to {logging_level}")
        elif logging_level == 'WARNING':
            logger.setLevel(logging.WARNING)
            logger.warning(f"Logging level set to {logging_level}")
        elif logging_level == 'ERROR':
            logger.setLevel(logging.ERROR)
            logger.error(f"Logging level set to {logging_level}")
        elif logging_level == 'CRITICAL':
            logger.setLevel(logging.CRITICAL)
            logger.critical(f"Logging level set to {logging_level}")
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
    
    def closeEvent(self, event):
        self.settings.setValue('size', self.size())
        self.settings.setValue('pos', self.pos())
        event.accept()
    
if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
