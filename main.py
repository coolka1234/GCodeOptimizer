import os
from src.backend import constants
import traceback
from src.backend import global_vars
from src.gui.main_window import Ui_MainWindow
from src.gui.LogsWindow import LogsWindows
from src.backend.functions import get_and_write as main
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QSettings
from src.backend.local_logging import logger, err_logger, inf_logger, remove_logs
import logging

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButtonChooseFile.clicked.connect(self.open_file)
        self.pushButtonChooseSave.clicked.connect(self.choose_save_path)
        self.pushButtonConfirm.clicked.connect(self.execute)
        self.pushButton.clicked.connect(self.display_info)
        self.pushButtonInfoLogs.clicked.connect(self.open_logs)
        self.pushButtonErrorLogs.clicked.connect(self.open_err_logs)
        self.pushButtonClear.clicked.connect(self.clear)
        self.comboBoxLoggingLevel.currentIndexChanged.connect(self.set_logging_level)
        self.comboBoxLanguage.currentIndexChanged.connect(self.set_language)
        self.initialize_log_combobox()
        self.initialize_language_combobox()
        self.initialize_thresholds()
        self.settings=QSettings('settings.ini', QSettings.Format.IniFormat)
        self.load_settings()
        self.resize(self.settings.value('size', self.size()))
        self.move(self.settings.value('pos', self.pos()))
        
   
    def open_file(self):
        self.lineEditFilePath.setText(QFileDialog.getOpenFileName()[0])
    
    def choose_save_path(self):
        self.lineEditSavePath.setText(QFileDialog.getExistingDirectory(self, 'Choose save path'))
    
    def execute(self):
        save_path= self.lineEditSavePath.text()
        file_path= self.lineEditFilePath.text()
        file_name = self.lineEditFileName.text()
        if file_name.endswith('.nc'):
            logger.debug('File name already has .nc extension')
            file_name = file_name[:-3]
            logger.debug(f'File name changed to {file_name}')
        self.set_thresholds()
        if file_path == '':
            QMessageBox.critical(self, 'Error', 'Please choose a file')
            err_logger.error('No file chosen')
            return
        if not file_path.endswith('.nc'):
            QMessageBox.critical(self, 'Error', 'The file is not a .nc file')
            err_logger.error('File is not a .nc file')
            return
        if not os.path.exists(file_path):
            QMessageBox.critical(self, 'Error', 'The file does not exist')
            err_logger.error('File does not exist')
            return
        if not os.path.exists(save_path) and save_path != '' and not os.path.isdir(save_path):
            QMessageBox.critical(self, 'Error', 'The save path does not exist or is not a directory')
            err_logger.error('Save path does not exist or is not a directory')
            return
        if save_path == '' and file_name == '':
            save_path = file_path.replace('.nc', '_processed.nc')
            err_logger.warning(f"Save path not provided, saving to {save_path}")
        elif save_path == '' and file_name != '':
            save_path = replace_last_location_in_path(file_path, file_name)
        elif save_path != '' and file_name == '':
            save_path = os.path.join(save_path, os.path.basename(file_path).replace('.nc', '_processed.nc'))
        else:
            save_path = os.path.join(save_path, file_name + '.nc')
        if not save_path.endswith('.nc'):
            save_path = save_path + '.nc'
        if (os.path.exists(save_path)):
            reply = QMessageBox.question(self, 'Warning', 'File with the same name already exists in the save path. Do you want to overwrite it?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                err_logger.error('File with the same name already exists in the save path. Overwrite not confirmed')
                return
        try:
            logger.debug(f'Processing file {file_path} and saving to {save_path}')
            main(file_path, save_path, self.progressBar) 
            QMessageBox.information(self, 'Success', 'File processed successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', 'Error processing file')
            err_logger.error(f'Error processing file: {e}, traceback: {traceback.format_exc()}')

    def open_logs(self):
        list_of_lines=[]
        try:
            f=open('logs/info.log')
            list_of_lines=f.readlines()
            f.close()
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'No logs found')
            return
        self.logs_window = LogsWindows(list_of_lines)
        self.logs_window.show()
    
    def open_err_logs(self):
        list_of_lines=[]
        try:
            f=open('logs/error.log')
            list_of_lines=f.readlines()
            f.close()
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'No logs found')
            return
        self.logs_window = LogsWindows(list_of_lines)
        self.logs_window.show()

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
    
    def initialize_language_combobox(self):
        self.comboBoxLanguage.addItems(constants.languages)
        self.comboBoxLanguage.setCurrentText('English')
    
    def initialize_thresholds(self):
        self.comboBoxA.addItems(constants.logging_levels)
        self.comboBoxF.addItems(constants.logging_levels)
        self.comboBoxS.addItems(constants.logging_levels)
        self.comboBoxX.addItems(constants.logging_levels)
        self.comboBoxY.addItems(constants.logging_levels)
        self.comboBoxZ.addItems(constants.logging_levels)
    
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
            self.lineEditFileName.setPlaceholderText('Processed file name (default is <original_file_name>_processed.nc)')
            self.pushButtonClear.setText('Clear')
        elif language == 'Polish':
            self.pushButtonChooseFile.setText('Wybierz plik')
            self.pushButtonChooseSave.setText('Wybierz ścieżkę zapisu')
            self.pushButtonConfirm.setText('Potwierdź')
            self.lineEditFilePath.setPlaceholderText('Plik do przetworzenia...')
            self.lineEditSavePath.setPlaceholderText('Lokalizacja zapisu...')
            self.labelLoggingLevel.setText('Wybierz poziom logowania:')
            self.lineEditFileName.setPlaceholderText('Nazwa przetworzonego pliku (domyślnie <oryginalna_nazwa_pliku>_processed.nc)')
            self.pushButtonClear.setText('Wyczyść')
            self.labelLanguage.setText('Wybierz język:')
        inf_logger.info(f"Language set to {language}")
    
    def set_thresholds(self):
        try:
            constants.A_log_level = self.comboBoxA.currentText()
            constants.A_threshold = None if self.lineEditMaxA.text()=='' else float(self.lineEditMaxA.text())
            constants.F_log_level = self.comboBoxF.currentText()
            constants.F_threshold = None if self.lineEditMaxF.text()==''else float(self.lineEditMaxF.text())
            constants.S_log_level = self.comboBoxS.currentText()
            constants.S_threshold =  None if self.lineEditMaxS.text()==''else float(self.lineEditMaxS.text())
            constants.X_log_level = self.comboBoxX.currentText()
            constants.X_threshold = None if self.lineEditMaxX.text()=='' else float(self.lineEditMaxX.text())
            constants.Y_log_level = self.comboBoxY.currentText()
            constants.Y_threshold = None if self.lineEditMaxY.text()=='' else float(self.lineEditMaxY.text())
            constants.Z_log_level = self.comboBoxZ.currentText()
            constants.Z_threshold = None if self.lineEditMaxZ.text()=='' else float(self.lineEditMaxZ.text())
        except ValueError as e:
            err_logger.error(f"Error setting thresholds: {e}")
            QMessageBox.critical(self, 'Error', 'Error setting thresholds. Please provide a valid number')
            return
        inf_logger.info(f"Thresholds set to A: {constants.A_threshold}, F: {constants.F_threshold}, S: {constants.S_threshold}, X: {constants.X_threshold}, Y: {constants.Y_threshold}, Z: {constants.Z_threshold}")
    
    def display_info(self):
        language = self.comboBoxLanguage.currentText()
        if language == 'English':
            QMessageBox.information(self, 'Info', constants.info_EN)
        elif language == 'Polish':
            QMessageBox.information(self, 'Info', constants.info_PL)
    
    def load_settings(self):
        self.comboBoxLoggingLevel.setCurrentText(self.settings.value('logging_level', 'DEBUG'))
        self.comboBoxLanguage.setCurrentText(self.settings.value('language', 'English'))
        self.lineEditFilePath.setText(self.settings.value('file_path', ''))
        self.lineEditSavePath.setText(self.settings.value('save_path', ''))
        self.lineEditMaxA.setText(self.settings.value('A_threshold', ''))
        self.lineEditMaxF.setText(self.settings.value('F_threshold', ''))
        self.lineEditMaxS.setText(self.settings.value('S_threshold', ''))
        self.lineEditMaxX.setText(self.settings.value('X_threshold', ''))
        self.lineEditMaxY.setText(self.settings.value('Y_threshold', ''))
        self.lineEditMaxZ.setText(self.settings.value('Z_threshold', ''))
        self.comboBoxA.setCurrentText(self.settings.value('A_log_level', 'DEBUG'))
        self.comboBoxF.setCurrentText(self.settings.value('F_log_level', 'DEBUG'))
        self.comboBoxS.setCurrentText(self.settings.value('S_log_level', 'DEBUG'))
        self.comboBoxX.setCurrentText(self.settings.value('X_log_level', 'DEBUG'))
        self.comboBoxY.setCurrentText(self.settings.value('Y_log_level', 'DEBUG'))
        self.comboBoxZ.setCurrentText(self.settings.value('Z_log_level', 'DEBUG'))
    
    def clear(self):
        self.lineEditFilePath.clear()
        self.lineEditSavePath.clear()
        self.lineEditFileName.clear()
        self.lineEditMaxA.clear()
        self.lineEditMaxF.clear()
        self.lineEditMaxS.clear()
        self.lineEditMaxX.clear()
        self.lineEditMaxY.clear()
        self.lineEditMaxZ.clear()
        self.comboBoxA.setCurrentText('WARNING')
        self.comboBoxF.setCurrentText('WARNING')
        self.comboBoxS.setCurrentText('WARNING')
        self.comboBoxX.setCurrentText('WARNING')
        self.comboBoxY.setCurrentText('WARNING')
        self.comboBoxZ.setCurrentText('WARNING')

    
    def closeEvent(self, event):
        self.settings.setValue('size', self.size())
        self.settings.setValue('pos', self.pos())
        self.settings.setValue('logging_level', self.comboBoxLoggingLevel.currentText())
        self.settings.setValue('file_path', self.lineEditFilePath.text())
        self.settings.setValue('save_path', self.lineEditSavePath.text())
        self.settings.setValue('language', self.comboBoxLanguage.currentText())
        self.settings.setValue('A_threshold', self.lineEditMaxA.text())
        self.settings.setValue('F_threshold', self.lineEditMaxF.text())
        self.settings.setValue('S_threshold', self.lineEditMaxS.text())
        self.settings.setValue('X_threshold', self.lineEditMaxX.text())
        self.settings.setValue('Y_threshold', self.lineEditMaxY.text())
        self.settings.setValue('Z_threshold', self.lineEditMaxZ.text())
        self.settings.setValue('A_log_level', self.comboBoxA.currentText())
        self.settings.setValue('F_log_level', self.comboBoxF.currentText())
        self.settings.setValue('S_log_level', self.comboBoxS.currentText())
        self.settings.setValue('X_log_level', self.comboBoxX.currentText())
        self.settings.setValue('Y_log_level', self.comboBoxY.currentText())
        self.settings.setValue('Z_log_level', self.comboBoxZ.currentText())
        event.accept()
    
def replace_last_location_in_path(path, new_location):
    head, _ = os.path.split(path)
    new_path = os.path.join(head, new_location)
    return new_path

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
