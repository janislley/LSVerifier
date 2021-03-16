#!/usr/bin/env python3

import subprocess
import logging 
import re
import shell
import shlex
import glob
import instrumenter

LOG_LINE = "log_line"
FILE = "file"
LINE = "line"
FUNCTION = "function"
PROPERTY = "property"
DIV_BY_ZERO = "division by zero"
FRAMA_C = "#ifdef __FRAMAC__\n\tFrama_C_show_each_{}({});\n#endif\n"
FRAMA_EVA = "frama-c -eva"
FRAMA_LOG = "output/frama.log"
PATTERN_FILE = "file (.*?) line "
PATTERN_LINE = "line (.*?) function"
PATTERN_FUNC = "function (.*?)$"

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
            counters[FILE] = re.search(PATTERN_FILE,i).group(1).strip()
            counters[LINE] = int(re.search(PATTERN_LINE,i).group(1).strip())
            counters[FUNCTION] = re.search(PATTERN_FUNC,i).group(1).strip()
            counters[PROPERTY] = j.strip()

            list_dict.append(counters)

    return list_dict

def cex_handler(cex):
    """docstring for cex_handler"""
    if DIV_BY_ZERO in cex.values():
        variable_line = read_lines("output/output.log",[cex[LOG_LINE]+1])
        variable = variable_line[0][0]
        """ TODO fix format """
        insert = FRAMA_C.format("lib_div", variable)

        insert_file(insert, cex[FILE], cex[LINE])

def insert_file(insert, fname, line):
    """docstring for insert_file"""
    with open(fname, "r+") as f:
        list_lines = f.readlines()
        list_lines.insert(line-1, insert)
        f.seek(0)
        f.writelines(list_lines)
    print("["+fname+"] Framac function inserted")

def run_frama(files):
    """docstring for run_frama"""
    cmd = shlex.split(FRAMA_EVA) + files
    with open(FRAMA_LOG, "w") as f:
        f.write(shell.run(cmd))
    print("Frama Log created")

def get_framac_output(cex):
    """docstring for get_framac_output"""
    if DIV_BY_ZERO in cex.values():
        framac_string = "Frama_C_show_each_{}".format(cex[FUNCTION])
        lines = search_in_file(FRAMA_LOG, framac_string)
        
        lines = [n-1 for n in lines]
        line_content = read_lines(FRAMA_LOG, lines)

        list_output = []
        for n in line_content:
            result = re.search(r"\{([0-9]+)\}", n)

            list_output.append(int(result.group(1)))

        return list_output
    
def main():
    print("Running...")
    
    fname = "output/output.log"
    string = "Violated property"

    # Find lines where "Violated property" is found
    cex_location_line = search_in_file(fname, string)
    print(str(len(cex_location_line))+" Violations")
    print("\nLog parsing...")

    # Read those lines
    cex_location = read_lines(fname, cex_location_line)
    
    # Increment Line to find the property
    prop_line = [n+1 for n in cex_location_line]
    # Read those line
    prop = read_lines(fname, prop_line)

    # Get all information about the counterexample and create a dictionary
    cex_dict = counter_to_dict(prop_line, cex_location, prop)

    # Check each counterexample type and insert Frama-c function
    print("\n--- Frama-C Instrumentation ---")
    for n in cex_dict:
        cex_handler(n)

    # Get all .c file and run Frama-c
    print("\n--- Running Frama-C ---")
    c_files =  glob.glob("*.c")
    run_frama(c_files)
    
    for n in cex_dict:
        framac_value = get_framac_output(n)

        if DIV_BY_ZERO in n.values():
            variable_line = read_lines("output/output.log",[n[LOG_LINE]+1])
            variable = variable_line[0][0]


            map = ({n[LINE]:[variable,framac_value]})

            instrumenter.instrument_code(n[FILE], map)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
