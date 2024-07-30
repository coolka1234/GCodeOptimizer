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
    a=operation_line.A
    f=operation_line.F
    x=operation_line.X
    radius=operation_line.Z
    
    # Convert A from degrees to radians
    a_rad = math.radians(a) if a is not None else 0
    # Calculate the linear distance for the angular movement
    distance_a = radius * a_rad
    # Calculate the total effective distance moved
    distance_x = x if x is not None else 0
    distance_z = z if z is not None else 0
    total_distance = math.sqrt(distance_x**2 + distance_a**2 + distance_z**2)
    # Adjust the feed rate
    if total_distance == 0:
        return f  # No movement, return the original feed rate
    adjusted_feed = f * distance_x / total_distance
    return adjusted_feed