import subprocess
import glob
import time
import argparse
import shlex
import sys
import os
from shutil import which
from src.csvwr import csvwr
from src.log import log
from src.bar import Bar
from pathlib import Path

CTAGS = "ctags"
CTAGS_TAB = "-x"
CTAGS_FUNC = "--c-types=f"

ESBMC = "esbmc"
FUNCTION = "--function"
NO_POINTER = "--no-pointer-check"

POINTER_FAIL = "invalid pointer"

DEP = "-I"

def get_command_line(args):
    cmd_line = ""

    if args.esbmc_parameter:
        para = args.esbmc_parameter
        para = para.split(" ")
        for i in range(len(para)):
            cmd_line += para[i] + " "

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

def run(cmd):
    invalid_pointer = 0
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    while True:
        out = proc.stdout.readline()

        if out == ''and proc.poll() is not None:
            break
        if out:
            log.info(out.strip())
            if POINTER_FAIL in out.strip():
                invalid_pointer = 1

    return invalid_pointer

def run_esbmc(c_file, cmd_line, dep_list, args):
    esbmc_args = []

    if not args.functions:
        func_list = ["main"]
    else:
        func_list = list_functions(c_file)

    esbmc_args = shlex.split(cmd_line);

    pbar = Bar(func_list, leave=False, verbose=args.verbose)
    for item in pbar:
        pbar.set_description("Processing %s" % item)
        log.header(c_file, esbmc_args, item)

        cmd = ([ESBMC, c_file] +
                ([] if not args.functions else [FUNCTION, item]) +
                dep_list +
                esbmc_args)

        fail = run(cmd)

        if args.retest_pointer:
            if fail:
                cmd.append(NO_POINTER)
                log.header_reteste(c_file, esbmc_args, item)
                run(cmd)

        log.info("")

def list_c_files(recursive, directory):
    file_list = []

    if recursive:
        for path in Path(".").rglob("*.c"):
           file_list.append(str(path))
    elif directory:
        file_list = glob.glob(directory + "/*.c")
    else:
        file_list = glob.glob("*.c")

    if not len(file_list):
        log.error("There is not .c file here!!")
        sys.exit()

    return(file_list)

def arguments():
    parser = argparse.ArgumentParser("Input Options")
    parser.add_argument("-e", "--esbmc-parameter", help="Use ESBMC parameter")
    parser.add_argument("-i", "--libraries", help="Path to the file that describe the libraries dependecies", default=False)
    parser.add_argument("-f", "--functions", help="Enable Functions Verification", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", help="Enable Verbose Output", action="store_true", default=False)
    parser.add_argument("-r", "--recursive", help="Enable Recursive Verification", action="store_true", default=False)
    parser.add_argument("-d", "--directory", help="Set the directory to be verified", default=False)
    parser.add_argument("-fl", "--file", help="File to be verified", default=False)
    parser.add_argument("-rp", "--retest-pointer", help="Retest Invalid Pointer", action="store_true", default=False)
    args = parser.parse_args()

    return(args)

def is_esbmc_installed():
    if not which(ESBMC) is not None:
        print("ESBMC not found!!")
        sys.exit()

def main():
    is_esbmc_installed()

    args = arguments()

    log.configure(args.verbose)

    print("ESBMC Running...")

    # Format ESBMC arguments
    cmd_line = get_command_line(args)

    # Read Libraries Dependencies File
    if args.libraries:
        log.info("Dependecies File: %s" % args.libraries)
        dep_list = read_dep_file(args.libraries)
    else:
        dep_list = []

    # Get c files on the folder
    if args.file:
        all_c_files = [args.file]
    else:
        all_c_files = list_c_files(args.recursive, args.directory)


    start_all = time.time()

    pbar = Bar(all_c_files, verbose=args.verbose)
    # Run ESBMC on each file found
    for c_file in pbar:
        pbar.set_description("Processing %s" % c_file)
        start = time.time()

        run_esbmc(c_file, cmd_line, dep_list, args)

        elapsed = (time.time() - start)
        log.finish_time(c_file, elapsed)


    elapsed_all = (time.time() - start_all)
    log.overall_time(elapsed_all)

    # Run csvwr to export output to a spreadsheet
    csvwr.export_cex()
    print("Done!")

if __name__ == "__main__":
    main()
