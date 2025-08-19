#!/usr/bin/env python3
# above line is for Unix-like systems to use this script as an executable

import sys  # to handle command line arguments
import os  # to interact with the operating system

def handle_3_args(field, file):
    with open(file, 'r', encoding='utf-8') as f:
        field = int(field[2])-1
        for line in f:
            line = line.split()
            print(line[field])
            
def handle_4_args(field, delimiter, file):
    with open(file, 'r', encoding='utf-8') as f:
        field = int(field[2])-1
        delimiter = delimiter[2]
        for line in f:
            line = line.split(delimiter)
            print(line[field])

def main():
    if len(sys.argv) == 3:
        field, file = sys.argv[1], sys.argv[2]
        handle_3_args(field, file)
    elif len(sys.argv) == 4:
        field, delimiter, file = sys.argv[1], sys.argv[2], sys.argv[3]
        handle_4_args(field, delimiter, file)
    else:
        print("Error: wrong command")
        sys.exit(1)    

if __name__ == "__main__":
    main()