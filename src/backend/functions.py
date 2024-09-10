#functions.py
#This file contains the functions that are used to process the g-code files. 
import math
import os
from src.backend.file_operations import read_nc_file
import src.backend.global_vars as global_vars
from src.backend.local_logging import logger, inf_logger, err_logger
from src.backend.Operation import Operation
import regex as re

def get_and_write(file_path, save_path, progress_bar=None):
    """Get the file path and write the processed file using generator"""
    logger.debug(f"Processing file {file_path}")
    calculated_num_of_lines=number_of_lines(file_path)
    generator=read_nc_file(file_path=file_path)
    with open(save_path,'w', encoding='cp1250') as file:
        line_num=1
        for line in generator:
            if is_line_of_interest(line):
                logger.debug(f"I: {line.rstrip()}")
                new_line=handle_the_line(line)
                file.write(new_line)
            else:
                file.write(line)
                logger.debug(f"NI: {line.rstrip()}")
                handle_ni_line(line)
            if progress_bar is not None:
                progress_bar.setValue(int((line_num/calculated_num_of_lines)*100))
            line_num+=1
    logger.debug(f"File {file_path} processed")
    logger.debug(f"Processed file saved to {save_path}")
    inf_logger.info(f"Max X: {global_vars.max_X}, Min X: {global_vars.min_X}")
    inf_logger.info(f"Max Z: {global_vars.max_Z}, Min Z: {global_vars.min_Z}")
    inf_logger.info(f"Max A: {global_vars.max_A}, Min A: {global_vars.min_A}")
    inf_logger.info(f"Max Y: {global_vars.max_Y}, Min Y: {global_vars.min_Y}")
    inf_logger.info(f"Max S: {global_vars.max_S}, Min S: {global_vars.min_S}")
    inf_logger.info(f"Max F: {global_vars.max_F}, Min F: {global_vars.min_F}")
    inf_logger.info(f"Max processed F: {global_vars.max_proc_F}, Min processed F: {global_vars.min_proc_F}")


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
    if not('G01' in line or global_vars.global_operation == 'G01' or global_vars.global_operation == 'G02'):
        return False
    if 'G53' in line:
        return False
    pattern = r'[AXYZ]'
    return bool(re.search(pattern, line))
 
def calculate_F(line):
    """Calculate the optimized F value for the line"""
    operation_line=Operation(line)
    A=operation_line.A
    F=operation_line.F if operation_line.F is not None else global_vars.global_F
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
            check_max_proc_F(adjusted_F)
            return round(adjusted_F,1)
    else:
        distance = math.sqrt(X**2 + (arc_length)**2)
    if distance != 0:
        adjusted_F = F / distance * abs(X)
        logger.debug(f"Distance: {distance} for X: {X}, Z: {Z}, A: {A}, F: {F}, arc_length: {arc_length}, new F: {round(adjusted_F,1)}")
    else:
        adjusted_F = F
    check_max_proc_F(adjusted_F)
    return round(adjusted_F,1)

def check_max_proc_F(F):
    """Check the maximum processed F value"""
    if F > global_vars.max_proc_F:
        global_vars.max_proc_F = F
    if F < global_vars.min_proc_F:
        global_vars.min_proc_F = F

def replace_f_in_line(f_value, line):
    """Replace the F value in the line"""
    output_string = ""
    output_string += line
    logger.debug(f"String to replace F: {output_string}, F: {f_value}")
    if 'F' not in line:
        new_F= 'F'+str(f_value)
        logger.debug(f"New F: {new_F}")
        output_string = insert_after_last_digit(output_string, new_F)
        logger.debug(f"New F inputted: {output_string}")
    else:
        output_string = re.sub(r'F\d+(\.\d+)?', 'F'+str(f_value), line)
        logger.debug(f"New F replaced: {output_string}")
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

def handle_ni_line(line):
    """Handle the line that is not of interest"""
    operation=Operation(line, only_analyze=True)
    operation.handle_maxes(operation.parse_line(line))

def insert_after_last_digit(input_string, string_to_insert):
    match = re.search(r'\d(?!.*\d)', input_string)
    if match:
        position = match.end()
        return input_string[:position] + string_to_insert + input_string[position:]
    else:
        return input_string

def number_of_lines(path):
    try:
        with open(path, "rb") as f:
            num_lines = sum(1 for _ in f)
        logger.debug(f"Number of lines in the file: {num_lines}")
        return num_lines
    except Exception as e:
        err_logger.error(f"Error counting lines: {e}")
        return 0
