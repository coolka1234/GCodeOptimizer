# Operation.py
# Class to handle each operation line
import regex as re
import src.backend.global_vars as global_vars
from src.backend.local_logging import inf_logger, logger, err_logger
from src.backend import constants
import logging
class Operation:
    def __init__(self, line, only_analyze=False) -> None:
        """Initialize the object with the values from the line"""
        dict_of_values= self.parse_line(line)
        self.X=None if dict_of_values['X']==None else float(dict_of_values['X'][1:]) - global_vars.global_X
        self.Z=global_vars.global_Z if dict_of_values['Z']==None else float(dict_of_values['Z'][1:])
        self.A=None if dict_of_values['A']==None else float(dict_of_values['A'][1:]) - global_vars.global_A
        self.S=None if dict_of_values['S']==None else float(dict_of_values['S'][1:])
        self.F=global_vars.global_F if dict_of_values['F']==None else float(dict_of_values['F'][1:])
        self.Y=None if dict_of_values['Y']==None else float(dict_of_values['Y'][1:])
        self.operation=global_vars.global_operation if dict_of_values['operation']==None else dict_of_values['operation']
        if only_analyze:
            global_vars.global_F=self.F
            return
        global_vars.global_Z=self.Z
        if self.operation is not None:
            global_vars.global_operation=self.operation
        if self.X is not None:
            global_vars.global_X=float(dict_of_values['X'][1:])
        if self.A is not None:
            global_vars.global_A=float(dict_of_values['A'][1:])
        if self.S is not None:
            global_vars.global_S=float(dict_of_values['S'][1:])
        if self.Y is not None:
            global_vars.global_Y=float(dict_of_values['Y'][1:])
        self.handle_maxes(dict_of_values)
        self.check_tresholds(dict_of_values)
        
        logger.debug(f"Operation: {self}")
    def parse_line(self,line):
        """Parse the line and return a dictionary of values using regex"""
        dict_of_values = {}
        operation_match = re.search(r'G\d+', line)
        dict_of_values['operation'] = operation_match.group(0) if operation_match else None

        y_match = re.search(r'Y-?\d+(\.\d+)?', line)
        dict_of_values['Y'] = y_match.group(0) if y_match else None

        x_match = re.search(r'X-?\d+(\.\d+)?', line) 
        dict_of_values['X'] = x_match.group(0) if x_match else None
        
        z_match = re.search(r'Z-?\d+(\.\d+)?', line)
        dict_of_values['Z'] = z_match.group(0) if z_match else None
        
        a_match = re.search(r'A-?\d+(\.\d+)?', line)
        dict_of_values['A'] = a_match.group(0) if a_match else None
        
        f_match = re.search(r'F-?\d+(\.\d+)?', line)
        dict_of_values['F'] = f_match.group(0) if f_match else None
        s_match= re.search(r'S-?\d+(\.\d+)?', line)
        dict_of_values['S'] = s_match.group(0) if s_match else None
        logger.debug(f"Dict of values: {dict_of_values}")
        return dict_of_values

    def __str__(self) -> str:
        """Return the string representation of the object"""
        return f'X: {self.X}, Z: {self.Z}, A: {self.A}, F: {self.F}, Operation: {self.operation}'    
    
    def check_tresholds(self, dict_of_values):
        """Check if the values are above the tresholds"""
        if constants.X_threshold is not None and dict_of_values['X'] is not None:
            if self.X > constants.X_threshold:
                logger.log(getattr(logging, constants.X_log_level),f"X value above threshold: {self.X}")
                err_logger.log(getattr(logging, constants.X_log_level), f"X value above threshold {self.X}")
        if constants.Z_threshold is not None and dict_of_values['Z'] is not None:
            if self.Z > constants.Z_threshold:
                logger.log(getattr(logging, constants.Z_log_level),f"Z value above threshold: {self.Z}")
                err_logger.log(getattr(logging, constants.Z_log_level), f"Z value above threshold {self.Z}")
        if constants.A_threshold is not None and dict_of_values['A'] is not None:
            if self.A > constants.A_threshold:
                logger.log(getattr(logging, constants.A_log_level),f"A value above threshold: {self.A}")
                err_logger.log(getattr(logging, constants.A_log_level), f"A value above threshold {self.A}")
        if constants.F_threshold is not None and dict_of_values['F'] is not None:
            if self.F > constants.F_threshold:
                logger.log(getattr(logging, constants.F_log_level),f"F value above threshold: {self.F}")
                err_logger.log(getattr(logging, constants.F_log_level), f"F value above threshold {self.F}")
        if constants.S_threshold is not None and dict_of_values['S'] is not None:
            if self.S > constants.S_threshold:
                logger.log(getattr(logging, constants.S_log_level),f"S value above threshold: {self.S}")
                err_logger.log(getattr(logging, constants.S_log_level), f"S value above threshold {self.S}")
            
    
    def handle_maxes(self, dict_of_values):
        """Handle the maximum and minimum values"""
        if dict_of_values['X'] is not None:
            if self.X > global_vars.max_X:
                global_vars.max_X=self.X
            if self.X < global_vars.min_X:
                global_vars.min_X=self.X
        if dict_of_values['Z'] is not None:
            if self.Z > global_vars.max_Z:
                global_vars.max_Z=self.Z
            if self.Z < global_vars.min_Z:
                global_vars.min_Z=self.Z
        if dict_of_values['A'] is not None:
            if self.A > global_vars.max_A:
                global_vars.max_A=self.A
            if self.A < global_vars.min_A:
                global_vars.min_A=self.A
        if dict_of_values['F'] is not None:
            if self.F > global_vars.max_F:
                global_vars.max_F=self.F
            if self.F < global_vars.min_F:
                global_vars.min_F=self.F
        if dict_of_values['S'] is not None:
            if self.S > global_vars.max_S:
                global_vars.max_S=self.S
            if self.S < global_vars.min_S:
                global_vars.min_S=self.S
        if dict_of_values['Y'] is not None:
            if self.Y > global_vars.max_Y:
                global_vars.max_Y=self.Y
            if self.Y < global_vars.min_Y:
                global_vars.min_Y=self.Y
 