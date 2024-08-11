import regex
import sys
import os
from functions import get_and_write

def main():
    if len(sys.argv) < 2:
        print("Usage: python optimize_gcode.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist")
        sys.exit(1)
    # get_and_write(input_file)

if __name__ == '__main__':
    main() 