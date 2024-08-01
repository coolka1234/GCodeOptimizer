from fileinput import filename
import logging
from venv import logger

def get_logger():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(filename='./logs/log.log',level=logging.DEBUG, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = get_logger()
