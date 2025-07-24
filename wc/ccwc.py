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
        sys.exit(1)
    except IOError:
        print("Error reading file.")
        sys.exit(1)
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
        sys.exit(1)
    except IOError:
        print("Error reading file.")
        sys.exit(1)
    return 

def count_words(file_path):
    # open file
    word_count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f: # read without binary
            for line in f:
                line = line.split()
                word_count += len(line)
        return word_count
    except FileNotFoundError:
        print("Please provide a valid file.")
        sys.exit(1)
    except IOError:
        print("Error reading file.")
        sys.exit(1)
    return 

def count_chars(file_path):
    # open file
    char_count = 0
    try:
        with open(file_path, 'rb') as f: # open as binary to get all chars (not just utf-8)
            all_bytes = f.read()
        i = 0
        while i < len(all_bytes):
            curr_byte = all_bytes[i]
            if (curr_byte & 0x80) == 0x00:
                i += 1
            elif (curr_byte & 0xE0) == 0xC0:
                i += 2
            elif (curr_byte & 0xF0) == 0xE0:
                i += 3
            elif (curr_byte & 0xF8) == 0xF0:
                i += 4
            else:
                i += 1
            char_count += 1
        return char_count
    except FileNotFoundError:
        print("Please provide a valid file.")
        sys.exit(1)
    except IOError:
        print("Error reading file.")
        sys.exit(1)
    return 

def handle_3_args(command, file):
    if command == '-c':
        byte_count = count_bytes(file)
        print(f"{byte_count}\t{file}") # Standard wc output format: count TAB filename
    elif command == '-l':
        line_count = count_lines(file)
        print(f"{line_count}\t{file}")
    elif command == '-w':
        word_count = count_words(file)
        print(f"{word_count}\t{file}")
    elif command == '-m':
        char_count = count_chars(file)
        print(f"{char_count}\t{file}")
    else:
        print(f"ccwc: invalid option -- '{command}'", file=sys.stderr)
        print("Try 'ccwc --help' for more information.", file=sys.stderr)
        sys.exit(1)

def handle_fileonly(file):
    byte_count = count_bytes(file)
    line_count = count_lines(file)
    word_count = count_words(file)
    print(f"{byte_count}\t{line_count}\t{word_count}\t{file}")

def handle_cmdonly(option):
    content_stream = sys.stdin
    if option == '-l':
            count = 0
            for _ in content_stream:
                count += 1
            print(count)

        elif option == '-w':
            count = 0
            for line in content_stream:
                words_in_line = line.split()
                count += len(words_in_line)
            print(count)

        elif option == '-c':
            byte_count = 0
            for byte_chunk in sys.stdin.buffer:
                byte_count += len(byte_chunk)
            print(byte_count)
            
        elif option == '-m':
            char_count = 0
            for line in content_stream:
                char_count += len(line)
            print(char_count)

        else:
            print(f"ccwc: invalid option -- '{option}'", file=sys.stderr)
            sys.exit(1)

def main():
    if len(sys.argv) == 3:
        command, file = sys.argv[1], sys.argv[2]
        handle_3_args(command, file)
    elif len(sys.argv == 2):
        option = sys.argv[1]
        if option == '-l' or option == '-w' or option == '-c' or option == '-m':
            handle_cmdonly(option)
        else:
            handle_fileonly(option)
    else:
        print("Error: wrong command")
        sys.exit(1)    

if __name__ == "__main__":
    main()