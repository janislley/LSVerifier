#!/usr/bin/env python3

import subprocess
import logging 
import re
import shell
import shlex
import glob

LOG_LINE = "log_line"
FILE = "file"
LINE = "line"
FUNCTION = "function"
PROPERTY = "property"
DIV_BY_ZERO = "division by zero"
FRAMA_C = "#ifdef __FRAMAC__\n\tFrama_C_show_each_{}({});\n#endif\n"
FRAMA_EVA = "frama-c -eva"
FRAMA_LOG = "output/frama.log"

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

def counter_to_dict(cex_line, cex, prop):
    """docstring for dict_counter"""
    list_dict = []
    for x, i, j in zip(cex_line, cex, prop):
        if not (len(i) == 0):
            counters = {}
            counters[LOG_LINE] = x
            counters[FILE] = i.split()[1]
            counters[LINE] = int(i.split()[3])
            counters[FUNCTION] = i.split()[5]
            counters[PROPERTY] = j.strip()

            list_dict.append(counters)

    return list_dict

def cex_handler(cex):
    """docstring for cex_handler"""
    if DIV_BY_ZERO in cex.values():
        variable_line = read_lines("output/output.log",[cex[LOG_LINE]+1])
        variable = variable_line[0][0]
        insert = FRAMA_C.format("lib_div", variable)

        insert_file(insert, cex[FILE], cex[LINE])

def insert_file(insert, fname, line):
    """docstring for insert_file"""
    with open(fname, "r+") as f:
        list_lines = f.readlines()
        list_lines.insert(line-1, insert)
        f.seek(0)
        f.writelines(list_lines)
    print("File changed")

def run_frama(files):
    """docstring for run_frama"""
    cmd = shlex.split(FRAMA_EVA) + files
    with open(FRAMA_LOG, "w") as f:
        f.write(shell.run(cmd))
    print("Frama Log created")
    
         
def main():
    print("Running...")
    
    fname = "output/output.log"
    string = "Violated property"

    cex_location_line = search_in_file(fname, string)
    cex_location = read_lines(fname, cex_location_line)
    
    prop_line = [n+1 for n in cex_location_line]
    prop = read_lines(fname, prop_line)

    cex_dict = counter_to_dict(prop_line, cex_location, prop)

    for n in cex_dict:
        cex_handler(n)

    c_files =  glob.glob("*.c")
    run_frama(c_files)

if __name__ == "__main__":
    main()
