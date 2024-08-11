#functions.py
#This file contains the functions that are used to process the g-code files. 
import math
import os
from src.backend.file_operations import read_nc_file
import src.backend.global_vars as global_vars
from src.backend.local_logging import logger
from src.backend.Operation import Operation
import regex as re
def get_and_write(file_path, save_path):
    """Get the file path and write the processed file using generator"""
    logger.debug(f"Processing file {file_path}")
    save_path = save_path + '/' +os.path.basename(file_path) +'_processed.nc'
    generator=read_nc_file(file_path=file_path)
    with open(save_path,'w', encoding='cp1250') as file:
        for line in generator:
            if is_line_of_interest(line):
                logger.debug(f"I: {line.rstrip()}")
                new_line=handle_the_line(line)
                file.write(new_line)
            else:
                file.write(line)
                logger.debug(f"NI: {line.rstrip()}")
    logger.debug(f"File {file_path} processed")

def is_line_of_interest(line):
    """Check if the line is of interest"""
    if '(' in line or ')' in line:
        return False
    if 'G00' in line:
        global_vars.global_operation='G00' 
        return False
    if 'G53' in line:
        global_vars.global_operation='G53'
        return False
    if not('G01' in line or 'G02' in line or global_vars.global_operation == 'G01' or global_vars.global_operation == 'G02'):
        return False
    if 'G53' in line:
        return False
    pattern = r'[AXYZ]'
    return bool(re.search(pattern, line))
 
def calculate_F(line):
    """Calculate the optimized F value for the line"""
    operation_line=Operation(line)
    A=operation_line.A
    F=operation_line.F
    X=operation_line.X
    Z=operation_line.Z
    arc_length=0 
    if Z==0 and A is None and X is None:
        return F 
    if A is not None:
        arc_length = abs(A)*Z*(math.pi/180)
    if X is None or X == 0:
        #formula for straight line
        adjusted_F = (F*180)/(math.pi*Z)
        if adjusted_F != 0:
            return round(adjusted_F,1)
    else:
        distance = math.sqrt(X**2 + (arc_length)**2)
    if distance != 0:
        adjusted_F = F / distance * abs(X)
        logger.debug(f"Distance: {distance} for X: {X}, Z: {Z}, A: {A}, F: {F}, arc_length: {arc_length}, new F: {adjusted_F}")
    else:
        adjusted_F = F
    
    return round(adjusted_F,1)

def replace_f_in_line(f_value, line):
    """Replace the F value in the line"""
    output_string = ""
    output_string += line
    # logger.debug(f"String to replace F: {output_string}, F: {f_value}")
    if 'F' not in line:
        new_F= 'F'+str(f_value)
        logger.debug(f"New F: {new_F}")
        output_string = insert_after_last_digit(output_string, new_F)
        # logger.debug(f"New F inputted: {output_string}")
    else:
        output_string = re.sub(r'F\d+(\.\d+)', 'F'+str(f_value), line)
        # logger.debug(f"New F replaced: {output_string}")
    logger.debug(f"Old line: {line.rstrip()}")
    logger.debug(f"New line: {output_string.rstrip()}\n")
    # output_string=re.sub(r'\.(?!\d)', '', output_string)
    if output_string.rstrip()[-1] == '.':
        output_string = output_string.rstrip()[:-1]
        output_string = output_string + '\n'
    return output_string

def handle_the_line(line):
    """Handle the line and return the new line"""
    F=calculate_F(line)
    new_line=replace_f_in_line(F, line)
    return new_line

def insert_after_last_digit(input_string, string_to_insert):
    match = re.search(r'\d(?!.*\d)', input_string)
    if match:
        position = match.end()
        return input_string[:position] + string_to_insert + input_string[position:]
    else:
        return input_string