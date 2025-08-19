#!/usr/bin/env python3
# above line is for Unix-like systems to use this script as an executable

import sys  # to handle command line arguments
import os  # to interact with the operating system

def handle_3_args(field, file):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split()
            print(line[1])

def main():
    if len(sys.argv) == 3:
        field, file = sys.argv[1], sys.argv[2]
        handle_3_args(field, file)
    # elif len(sys.argv == 2):
    #     option = sys.argv[1]
    #     if option == '-l' or option == '-w' or option == '-c' or option == '-m':
    #         handle_cmdonly(option)
    #     else:
    #         handle_fileonly(option)
    else:
        print("Error: wrong command")
        sys.exit(1)    

if __name__ == "__main__":
    main()