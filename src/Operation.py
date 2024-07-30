import regex as re
class Operation:
    def __init__(self, line) -> None:
        dict_of_values= self.parse_line(line)
        # print(dict_of_values)
        self.X=None if None else float(dict_of_values['X'][1:])
        self.Z=None if None else float(dict_of_values['Z'][1:])
        self.A=None if None else float(dict_of_values['A'][1:])
        self.F=None if None else float(dict_of_values['F'][1:])
        self.operation=None if None else dict_of_values['operation']

    def parse_line(self,line):
        dict_of_values = {}
        dict_of_values['operation'] = re.search(r'[A-Z]\d+', line).group(0)
        dict_of_values['X'] = re.search(r'X\d+\.\d+', line).group(0)
        dict_of_values['Z'] = re.search(r'Z\d+\.\d+', line).group(0)
        dict_of_values['A'] = re.search(r'A\d+\.\d+', line).group(0)
        dict_of_values['F'] = re.search(r'F\d+\.\d+', line).group(0)
        return dict_of_values

    def __str__(self) -> str:
        return f'X: {self.X}, Z: {self.Z}, A: {self.A}, F: {self.F}, Operation: {self.operation}'    
print(str(Operation('G01X114.6109Z27.0517A18.8177674F1600.0')))
 