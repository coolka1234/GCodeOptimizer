from math import log
import math
from file_operations import read_nc_file
import global_vars
from local_logging import logger
from Operation import Operation
import regex as re
def get_and_write(file_path):
    logger.debug(f"Processing file {file_path}")
    generator=read_nc_file(file_path=file_path)
    with open(file_path.replace('.nc','processed.nc'),'w', encoding='cp1250') as file:
        for line in generator:
            if is_line_of_interest(line):
                logger.debug(f"I: {line}")
                new_line=handle_the_line(line)
                file.write(new_line)
            else:
                file.write(line)
                logger.debug(f"NI: {line}")
    logger.debug(f"File {file_path} processed")

def is_line_of_interest(line):
    if '(' in line or ')' in line:
        return False
    pattern = r'[AXYZ]'
    return bool(re.search(pattern, line))
 
def calculate_F(line):
    operation_line=Operation(line)
    A=operation_line.A
    F=operation_line.F
    X=operation_line.X
    Z=operation_line.Z
    effective_radius = Z
    if X is None or X == 0:
        effective_radius = Z
        distance = abs(effective_radius * A)
    else:
        effective_radius = Z
        distance = math.sqrt(X**2 + (effective_radius * A)**2)
    if distance != 0:
        adjusted_F = F / distance * global_vars.global_X
        logger.debug(f"Distance: {distance} for X: {X}, Z: {Z}, A: {A}, F: {F}")
    else:
        adjusted_F = F
    
    return round(adjusted_F,1)

def replace_f_in_line(f_value, line):
    output_string = re.sub(r'F\d+(\.\d+)?', 'F'+str(f_value), line)
    logger.debug(f"Old line: {line}")
    logger.debug(f"New line: {output_string}")
    return output_string

def handle_the_line(line):
    F=calculate_F(line)
    new_line=replace_f_in_line(F, line)
    return new_line