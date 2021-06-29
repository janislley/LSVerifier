import sys
import subprocess
import glob
from shutil import which
from pathlib import Path
from esbmc_wr.log import log

ESBMC = "esbmc"
CTAGS = "ctags"
CTAGS_TAB = "-x"
CTAGS_FUNC = "--c-types=f"

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

def is_esbmc_installed():
    if not which(ESBMC) is not None:
        print("ESBMC not found!!")
        sys.exit()
