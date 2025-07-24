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

def main():
    if len(sys.argv) < 3: # not enough arguments
        print("Usage: ccwc -c <file>")
        sys.exit
    command, file = sys.argv[1], sys.argv[2]
    
    if command == '-c':
        byte_count = count_bytes(file)
        print(f"{byte_count}\t{file}") # Standard wc output format: count TAB filename
    else:
        print(f"ccwc: invalid option -- '{command}'", file=sys.stderr)
        print("Try 'ccwc --help' for more information.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()