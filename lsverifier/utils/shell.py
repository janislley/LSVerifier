import shlex
import subprocess
from pkg_resources import resource_filename
from lsverifier.utils import utils
from lsverifier.log import log
from lsverifier.bar import Bar
from lsverifier.analysis.analysis import get_prioritized_functions

ESBMC = "esbmc"
FUNCTION = "--function"
NO_POINTER = "--no-pointer-check"
POINTER_FAIL = "invalid pointer"

def get_esbmc_path():
   return resource_filename('lsverifier','bin/')

def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    ok = 0; invalid_pointer = 1;

    while True:
        out = proc.stdout.readline()

        if out == ''and proc.poll() is not None:
            break;
        if out:
            log.info(out.strip())
            if POINTER_FAIL in out.strip():
                return invalid_pointer;

    return ok;

def run_esbmc(c_file, cmd_line, dep_list, args):
    esbmc_args = []

    esbmc_path = get_esbmc_path() + ESBMC

    if not args.functions and not args.function_prioritized:
        func_list = ["main"]
    elif args.functions:
        func_list = utils.list_functions(c_file)
    elif args.function_prioritized:
        func_list = get_prioritized_functions(c_file)

    esbmc_args = shlex.split(cmd_line);

    #print("Functions to be analysed: ", func_list)

    # check a set of properties if any passed as an argument
    if args.properties:
        for prop in args.properties:
            esbmc_args.append(f"--{prop}")

    for func in func_list:
        log.header(c_file, esbmc_args, func)

        cmd = ([esbmc_path, c_file] +
                ([] if not args.functions else [FUNCTION, func]) +
                dep_list +
                esbmc_args)

        fail = run(cmd)

        if args.retest_pointer:
            if fail:
                cmd.append(NO_POINTER)
                log.header_retest(c_file, esbmc_args, func)
                run(cmd)

        log.info("")

    return len(func_list)
