#!/usr/bin/env python3

import subprocess
import logging 
import re

FILE = "file"
LINE = "line"
FUNCTION = "function"
PROPERTY = "property"

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

def counter_to_dict(line, prop):
    """docstring for dict_counter"""
    list_dict = []
    for i, j in zip(line, prop):
        if not (len(i) == 0):
            counters = {}
            counters[FILE] = i.split()[1]
            counters[LINE] = i.split()[3]
            counters[FUNCTION] = i.split()[5]
            counters[PROPERTY] = j.strip()

            list_dict.append(counters)

    return list_dict

def main():
    print("Running...")
    
    fname = "output/output.log"
    string = "Violated property"

    cex_location_line = search_in_file(fname, string)
    cex_location = read_lines(fname, cex_location_line)
    
    cex_line = [n+1 for n in cex_location_line]
    cex = read_lines(fname, cex_line)

    cex_dict = counter_to_dict(cex_location, cex)
    print(cex_dict)


if __name__ == "__main__":
    main()
