# local_logging.py:
# This file is used to create a logger object that can be used to log messages to a file and to the console.
import logging
from math import log
import os
#DEPRACATED
#############################################################################################################
def get_logger():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        if not os.path.exists('logs'):
            os.makedirs("logs")
        logging.basicConfig(filename='logs/debug.log',level=logging.DEBUG, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    except Exception as e:
        print("Error in creating log file: ", e)
        print("Program will continue attempt to log in current directory")
    try:
        logging.basicConfig(filename='log.log',level=logging.DEBUG, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    except Exception as e:
        print("Error in creating log file: ", e)
        print("Program will not log")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger 

def info_logger():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        if not os.path.exists('logs'):
            os.makedirs("logs")
        logging.basicConfig(filename='logs/info.log',level=logging.INFO, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    except Exception as e:
        print("Error in creating log file: ", e)
        print("Program will continue attempt to log in current directory")
    try:
        logging.basicConfig(filename='info.log',level=logging.INFO, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    except Exception as e:
        print("Error in creating log file: ", e)
        print("Program will not log")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def error_logger():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        if not os.path.exists('logs'):
            os.makedirs("logs")
        logging.basicConfig(filename='logs/error.log',level=logging.WARNING, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    except Exception as e:
        print("Error in creating log file: ", e)
        print("Program will continue attempt to log in current directory")
    try:
        logging.basicConfig(filename='error.log',level=logging.WARNING, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    except Exception as e:
        print("Error in creating log file: ", e)
        print("Program will not log")
    logger.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
#############################################################################################################

formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def setup_logger(name: str, log_file: str, level=logging.INFO):
    try:
        if not os.path.exists('logs'):
            os.makedirs("logs")
    except Exception as e:
        print("Error in creating log file: ", e)
        print("Program will continue attempt to log in current directory")
        log_file = log_file.split("/")[1]
    try:
        handler = logging.FileHandler(log_file, mode='w')
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
    except Exception as e:
        print("Error in creating log file: ", e)
        print("Program will not log")
        logger = logging.getLogger(name)
        logger.setLevel(logging.ERROR)
    return logger

def remove_logs():
    try:
        os.remove('logs/log.log')
        os.remove('logs/error.log')
        os.remove('logs/info.log')
    except Exception as e:
        print("Error in removing log files: ", e)

logger = setup_logger('logger', 'logs/log.log', logging.DEBUG)
err_logger = setup_logger('error_logger', 'logs/error.log', logging.WARNING)
inf_logger = setup_logger('info_logger', 'logs/info.log', logging.INFO)
