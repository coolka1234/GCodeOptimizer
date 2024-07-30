from math import log
import math
from file_operations import read_nc_file
from local_logging import logger
from Operation import Operation
import regex as re
def get_and_write(file_path):
    logger.debug(f"Processing file {file_path}")
    generator=read_nc_file(file_path=file_path)
    with open(file_path.replace('.nc','processed.nc'),'w', encoding='cp1250') as file:
        for line in generator:
            if is_line_of_interest(line):
                file.write(line)
                logger.debug(f"I: {line}")
            else:
                file.write(line)
                logger.debug(f"NI: {line}")
    logger.debug(f"File {file_path} processed")

def is_line_of_interest(line):
    pattern = r'(A-?\d+|F\d+)'
    return bool(re.search(pattern, line))

def calcualte_F(line):
    operation_line=Operation(line)
    A=operation_line.A
    F=operation_line.F
    X=operation_line.X
    Z=operation_line.Z
    effective_radius = Z
    distance = math.sqrt(X**2 + (effective_radius * A)**2)
    if F is not None:
        original_F = F
        F = original_F / distance * X if distance != 0 else original_F

def replace_f_in_line(f_value, line):
    output_string = re.sub(r'F\d+', 'F5678', line)