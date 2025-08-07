#!/usr/bin/env python3

import sys  # to handle command line arguments
import os  # to interact with the operating system
from collections import Counter

file_path = sys.argv[1]

try:
    with open(file_path, 'r') as f:
        # print freq of all chars
        all_bytes = f.read()
        res = Counter(all_bytes)
        print(res)
except FileNotFoundError:
    print("Please provide a valid file.")
    sys.exit(1)
except IOError:
    print("Error reading file.")
    sys.exit(1)