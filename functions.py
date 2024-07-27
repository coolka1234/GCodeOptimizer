from math import log
from file_operations import read_nc_file
from local_logging import logger
import regex as re
def get_and_write(file_path):
    logger.debug(f"Processing file {file_path}")
    generator=read_nc_file(file_path=file_path)
    with open(file_path.replace('.nc','processed.nc'),'w') as file:
        for line in generator:
            if is_line_of_interest(line):
                file.write(line)
                logger.debug(f"Line written: {line}")
    logger.debug(f"File {file_path} processed")

def is_line_of_interest(line):
    pattern = r'(A-?\d+|F\d+)'
    return bool(re.search(pattern, line))