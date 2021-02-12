#!/usr/bin/env python3

import subprocess
import logging 

CTAGS = "ctags"
FRAMA = "frama-c"
RTE =   "-rte"
PRINT = "-print"
THEN =  "-then"
OCODE = "-ocode" 
ACSL_OUT = "acsl_"

def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    
    while True:
        out = proc.stdout.readline()
        if out == '' and proc.poll() is not None:
            break
        if out:
            print(out.strip())

def generate_ACSL(cfile):
    run([FRAMA, RTE, cfile, PRINT, THEN, OCODE, ACSL_OUT+cfile])

def main():
    
    print("Running...")
    
    generate_ACSL("main.c")

if __name__ == "__main__":
    main()
