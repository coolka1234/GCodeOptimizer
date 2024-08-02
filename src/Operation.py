# Operation.py
# Class to handle each operation line
import regex as re
import global_vars
from local_logging import logger
class Operation:
    def __init__(self, line) -> None:
        """Initialize the object with the values from the line"""
        dict_of_values= self.parse_line(line)
        self.X=None if dict_of_values['X']==None else float(dict_of_values['X'][1:]) - global_vars.global_X
        self.Z=global_vars.global_Z if dict_of_values['Z']==None else float(dict_of_values['Z'][1:])
        logger.debug(f"Detected A: {dict_of_values['A']} global_A: {global_vars.global_A}")
        self.A=None if dict_of_values['A']==None else float(dict_of_values['A'][1:]) - global_vars.global_A
        self.F=global_vars.global_F if dict_of_values['F']==None else float(dict_of_values['F'][1:])
        self.operation=global_vars.global_operation if dict_of_values['operation']==None else dict_of_values['operation']
        global_vars.global_Z=self.Z
        global_vars.global_F=self.F
        if self.operation is not None:
            global_vars.global_operation=self.operation
        if self.X is not None:
            global_vars.global_X=float(dict_of_values['X'][1:])
        if self.A is not None:
            logger.debug(f"Global A: {global_vars.global_A}, local A: {self.A}")
            global_vars.global_A=float(dict_of_values['A'][1:])
        
        logger.debug(f"Operation: {self}")
    def parse_line(self,line):
        """Parse the line and return a dictionary of values using regex"""
        dict_of_values = {}
        dict_of_values['operation'] = re.search(r'[A-Z]\d+', line).group(0)
        x_match = re.search(r'X-?\d+(\.\d+)?', line) 
        dict_of_values['X'] = x_match.group(0) if x_match else None
        
        z_match = re.search(r'Z-?\d+(\.\d+)?', line)
        dict_of_values['Z'] = z_match.group(0) if z_match else None
        
        a_match = re.search(r'A-?\d+(\.\d+)?', line)
        dict_of_values['A'] = a_match.group(0) if a_match else None
        
        f_match = re.search(r'F-?\d+(\.\d+)?', line)
        dict_of_values['F'] = f_match.group(0) if f_match else None
        logger.debug(f"Dict of values: {dict_of_values}")
        return dict_of_values

    def __str__(self) -> str:
        """Return the string representation of the object"""
        return f'X: {self.X}, Z: {self.Z}, A: {self.A}, F: {self.F}, Operation: {self.operation}'    
 