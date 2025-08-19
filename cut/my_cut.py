#!/usr/bin/env python3
# above line is for Unix-like systems to use this script as an executable

import sys  # to handle command line arguments
import os  # to interact with the operating system

def handle_fields(field):
    # remove -f
    field = field[2:]
    # check if in quotes
    if "," in field:
        field = field.split(",")
    else:
        field = field.split()
    return field

def handle_3_args(field, file):
    with open(file, 'r', encoding='utf-8') as f:
        field = handle_fields(field)
        for line in f:
            line = line.split()
            op = ""
            for f in field:
                op += line[int(f)-1]
                op += " "
            print(op[:-1])
            
def handle_4_args(field, delimiter, file):
    with open(file, 'r', encoding='utf-8') as f:
        field = handle_fields(field)
        delimiter = delimiter[2]
        for line in f:
            op = ""
            line = line.split(delimiter)
            for f in field:
                op += line[int(f)-1]
                op += delimiter
            print(op[:-1])

def main():
    if len(sys.argv) == 3:
        field, file = sys.argv[1], sys.argv[2]
        handle_3_args(field, file)
    elif len(sys.argv) == 4:
        delimiter, field, file = sys.argv[1], sys.argv[2], sys.argv[3]
        handle_4_args(field, delimiter, file)
    else:
        print("Error: wrong command")
        sys.exit(1)    

if __name__ == "__main__":
    main()