#!/usr/bin/env python3

import subprocess
import glob
import time
import argparse
import shlex
import sys
import os
import sys

CTAGS = "ctags"
CTAGS_TAB = "-x"
CTAGS_FUNC = "--c-types=f"
ESBMC = "esbmc"
FUNCTION = "--function"
MEMORY_LEAK = "--memory-leak-check"
NO_POINTER = "--no-pointer-check"
OVERFLOW = "--overflow-check"
UNWIND = "--unwind"
UNWIND_NO = "--no-unwinding-assertions"
DEP = "-I"
INC_BMC = "--incremental-bmc"
K_INDUCTION = "--k-induction-parallel"
WITNESS = "--witness-output"
TIMEOUT = "--timeout"
DIRECTORY = "output"

def get_command_line(args):
    cmd_line = ""

    if args.memory_leak_check:
        cmd_line += MEMORY_LEAK + " "

    if args.unwind:
        cmd_line += UNWIND + " " + args.unwind + " "

    if args.timeout:
        cmd_line += TIMEOUT + " " + args.timeout + "s" + " "

    if args.no_unwinding_assertions:
        cmd_line += UNWIND_NO + " "

    if args.incremental_bmc:
        cmd_line += INC_BMC + " "

    if args.no_pointer_check:
        cmd_line += NO_POINTER + " "

    if args.overflow_check:
        cmd_line += OVERFLOW + " "

    if args.k_induction_parallel:
        cmd_line += K_INDUCTION

    return(cmd_line)

def read_dep_file(path):
    dep_file = open(path, "r")
    dep_list = [x.strip() for x in dep_file.readlines()]

    for i in range(len(dep_list)):
        dep_list.insert(2 * i, "-I")

    return(dep_list)

def list_functions(c_file):
    process = subprocess.Popen([CTAGS,CTAGS_TAB,CTAGS_FUNC,c_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)

    (stdout, stderr) = process.communicate()
    
    func_list = row_2_list(stdout) 
    func_list = find_main(func_list)

    return(func_list)

def row_2_list(text): 
    func = list()

    for row in text.split("\n"):
        if " " in row:
            key, value = row.split(" ",1)
            func.append(key)

    return(func)

def find_main(f_list):
    item = "main" 
    
    if item in f_list:
        f_list.insert(0, f_list.pop(f_list.index(item)))

    return(f_list)

def create_dir(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print("Directory ", name, " already exists.")
        sys.exit()

def run_esbmc(c_file, cmd_line, dep_list, time, func, witness):
    # Print file that will be checked
    print("[FILE] ",c_file)

    if not func:
        func_list = ["main"]
    else:
        # Get all function of c_file
        func_list = list_functions(c_file)
        esbmc_args = shlex.split(cmd_line);
        

    # Run ESBMC on each function of each file found
    for item in func_list:
        print("[FUNCTION] ",item, "\n") 

        output = subprocess.Popen([ESBMC, c_file] + 
            ([] if not func else [FUNCTION, item]) +
            ([] if not witness else [WITNESS, DIRECTORY + "/" + "graphML_" + item]) +
            esbmc_args + 
            dep_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)

        (stdout, stderr) = output.communicate()

        print(stdout)
        print(stderr)

def list_c_files():
    return(glob.glob("*.c"))

def main():
    # Input Parse
    parser = argparse.ArgumentParser("Input Options")
    parser.add_argument("-m", MEMORY_LEAK, help="Enable Memory Leak Check", action="store_true", default=False)
    parser.add_argument("-u", UNWIND, help="Enable Unwind")
    parser.add_argument("-nu", UNWIND_NO, help="Enable No Unwind Assertions", action="store_true", default=False)
    parser.add_argument("-ib", INC_BMC, help="Enable Incremental BMC", action="store_true", default=False)
    parser.add_argument("-p", NO_POINTER, help="Enable No Pointer Check", action="store_true", default=False)
    parser.add_argument("-o", OVERFLOW, help="Enable Overflow Check", action="store_true", default=False)
    parser.add_argument("-k", K_INDUCTION, help="Enable K Induction", action="store_true", default=False)
    parser.add_argument("-i", "--libraries", help="Path to the file that describe the libraries dependecies", default=False)
    parser.add_argument("-t", TIMEOUT, help="Set timeout in second")
    parser.add_argument("-f", "--functions", help="Enable Functions Verification", action="store_true", default=False)
    parser.add_argument("-w", WITNESS, help="Enable Witness Output", action="store_true", default=False)
    args = parser.parse_args()
    
    create_dir(DIRECTORY)
    
    print("ESBMC Running...", flush=True)
    
    # Init log file
    old_stdout = sys.stdout
    log_file = open(os.path.join(DIRECTORY, "output.log"),"w")
    sys.stdout = log_file

    # Format ESBMC arguments
    cmd_line = get_command_line(args)
    print("ESBMC Command Line: ", cmd_line)

    # Read Libraries Dependencies File
    if args.libraries:
        print("Dependecies File: ", args.libraries, "\n")
        dep_list = read_dep_file(args.libraries)
    else:
        dep_list = []

    # Get c files on the folder
    all_c_files = list_c_files()
    if not len(all_c_files):
        print("There is not .c file here!!", flush=True) 

    # Run ESBMC on each file found
    for c_file in all_c_files:
        start = time.time()
        
        run_esbmc(c_file, cmd_line, dep_list, args.timeout, args.functions, args.witness_output)

        elapsed = (time.time() - start)

        print("\n[FILE]: ",c_file," [TIME]: ",elapsed)  

    # Close log
    sys.stdout = old_stdout
    log_file.close()

    # Run csvwr to export output to a spreadsheet
    import csvwr
    print("Done!", flush=True)

if __name__ == "__main__":
    main()
