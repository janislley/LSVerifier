#!/usr/bin/env python3

import subprocess
import logging 
import re

CTAGS = "ctags"
FRAMA = "frama-c"
RTE =   "-rte"
PRINT = "-print"
THEN =  "-then"
OCODE = "-ocode" 
ACSL_OUT = "acsl_"

def search(fname, string):
    pattern = re.compile(string)
    line_number = 0
    lines = []

    for line in open(fname):
        line_number += 1
        for match in re.finditer(pattern, line):
            lines.append(line_number)
    
    return lines

def main():
    
    print("Running...")
    
    fname = "output/output.log"
    string = "VERIFICATION FAILED"

    print(search(fname, string))

if __name__ == "__main__":
    main()
