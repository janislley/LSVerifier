#!/usr/bin/env python3

import subprocess
import logging 
import re

FILE = "file"
LINE = "line"
FUNCTION = "function"

def search_in_file(fname, string):
    pattern = re.compile(string)
    line_number = 0
    lines = []

    for line in open(fname):
        line_number += 1
        for match in re.finditer(pattern, line):
            lines.append(line_number)
    
    return lines

def read_lines(fname, lines):
    """docstring for read_lines"""
    line_content = []
    with open(fname) as f:
        for pos, line in enumerate(f):
            if pos in lines:
                line_content.append(line.strip())

    return line_content

def counter_to_dict(location, prop):
    """docstring for dict_counter"""
    list_dict = []
    counters = {}
    for i in location:
        counters[FILE] = i.split()[1]
        counters[LINE] = i.split()[3]
        counters[FUNCTION] = i.split()[5]

        list_dict.append(counters)

    print(list_dict)

def main():
    
    print("Running...")
    
    fname = "output/output.log"
    string = "Counterexample"

    counter = search_in_file(fname, string)

    counter = [n+4 for n in counter]

    lines = read_lines(fname, counter)

    counter_to_dict(lines, 1)


if __name__ == "__main__":
    main()
