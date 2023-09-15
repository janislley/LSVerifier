import shlex
import subprocess
from pkg_resources import resource_filename
from lsverifier.utils import utils
from lsverifier.log import log
from lsverifier.bar import Bar
from lsverifier.analysis.analysis import get_prioritized_functions

ESBMC = "esbmc"
FUNCTION = "--function"
DISABLE_POINTER_CHECK = "--no-pointer-check"
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

    # Initialize func_list to an empty list or a default value
    func_list = []

    if not args.functions and not args.function_prioritized:
        func_list = ["main"]
    elif args.functions:
        func_list = utils.list_functions(c_file)
    elif args.function_prioritized:
        func_list = get_prioritized_functions(c_file)

    esbmc_args = shlex.split(cmd_line);

    # check a set of properties if any passed as an argument
    if args.properties:
        esbmc_args.clear()
        for prop in args.properties:
            esbmc_args.append(f"--{prop}")

    # show the list of functions to be analysed
    if args.verbose:
        print("Functions to be analysed: ", func_list)

    for func in func_list:
        log.header(c_file, esbmc_args, func)

        cmd = [esbmc_path, c_file] + dep_list + esbmc_args

        if args.functions or args.function_prioritized:
            cmd += [FUNCTION, func]
        
        fail = run(cmd)

        if args.disable_pointer_check:
            if fail:
                cmd.append(DISABLE_POINTER_CHECK)
                log.header_retest(c_file, esbmc_args, func)
                run(cmd)

        log.info("")

    return len(func_list)
