from fileinput import filename
import logging
from venv import logger

def get_logger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='log',level=logging.DEBUG, filemode='w')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = get_logger()
