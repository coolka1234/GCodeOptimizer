# local_logging.py:
# This file is used to create a logger object that can be used to log messages to a file and to the console.
from fileinput import filename
import logging
from venv import logger
import os
def get_logger():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        if not os.path.exists('logs/log.log'):
            os.makedirs("logs/log.log")
        logging.basicConfig(filename='logs/log.log',level=logging.DEBUG, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
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

logger = get_logger()
