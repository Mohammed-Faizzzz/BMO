#!/usr/bin/env python3
# above line is for Unix-like systems to use this script as an executable

import sys  # to handle command line arguments
import os  # to interact with the operating system

def count_bytes(file_path):
    # open file
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, os.SEEK_END) # Move to the end of the file
            byte_count = f.tell()  # Get the current position (which is the file size in bytes)
        return byte_count
    except FileNotFoundError:
        print("Please provide a valid file.")
        sys.exit
    except IOError:
        print("Error reading file.")
        sys.exit
    return 

def count_lines(file_path):
    # open file
    line_count = 0
    try:
        with open(file_path, 'rb') as f:
            for line in f:
                line_count += 1
        return line_count
    except FileNotFoundError:
        print("Please provide a valid file.")
        sys.exit
    except IOError:
        print("Error reading file.")
        sys.exit
    return 

def count_words(file_path):
    # open file
    word_count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f: # read without binary
            for line in f:
                line = line.split()
                # print(line)
                word_count += len(line)
        return word_count
    except FileNotFoundError:
        print("Please provide a valid file.")
        sys.exit
    except IOError:
        print("Error reading file.")
        sys.exit
    return 

def main():
    if len(sys.argv) < 3: # not enough arguments
        print("Usage: ccwc -c <file>")
        sys.exit
    command, file = sys.argv[1], sys.argv[2]
    
    if command == '-c':
        byte_count = count_bytes(file)
        print(f"{byte_count}\t{file}") # Standard wc output format: count TAB filename
    elif command == '-l':
        line_count = count_lines(file)
        print(f"{line_count}\t{file}")
    elif command == '-w':
        word_count = count_words(file)
        print(f"{word_count}\t{file}")
    else:
        print(f"ccwc: invalid option -- '{command}'", file=sys.stderr)
        print("Try 'ccwc --help' for more information.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()