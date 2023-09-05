import time
import argparse
import os
import tracemalloc
from lsverifier.csvwr import csvwr
from lsverifier.log import log
from lsverifier.bar import Bar
from lsverifier.utils import utils
from lsverifier.utils import shell

def arguments():
    parser = argparse.ArgumentParser("Input Options")
    parser.add_argument("-e", "--esbmc-parameter", help="Use ESBMC parameter")
    parser.add_argument("-i", "--libraries", help="Path to the file that describes the libraries dependencies", default=False)
    parser.add_argument("-f", "--functions", help="Enable Functions Verification", action="store_true", default=False)
    parser.add_argument("-fp", "--prioritized", help="Enable Prioritized Functions Verification", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", help="Enable Verbose Output", action="store_true", default=False)
    parser.add_argument("-r", "--recursive", help="Enable Recursive Verification", action="store_true", default=False)
    parser.add_argument("-d", "--directory", help="Set the directory to be verified", default=False)
    parser.add_argument("-p", "--propertyfile", help="Path to the property file", default=False)
    parser.add_argument("-fl", "--file", help="File to be verified", default=False)
    parser.add_argument("-rp", "--retest-pointer", help="Retest Invalid Pointer", action="store_true", default=False)
    args = parser.parse_args()

    return(args)

def main():

    print("LSVerifier is loading...")
    tracemalloc.start()

    args = arguments()
    print("Setting the verification parameters...")

    log_name = log.configure(args.verbose)

    print("Running ESBMC module verification...")

    cmd_line = utils.get_command_line(args)

    if args.libraries:
        log.info("Dependency files: %s" % args.libraries)
        dep_list = utils.read_dep_file(args.libraries)
    else:
        dep_list = []

    if args.file:
        all_c_files = [os.path.join(args.directory, args.file)]
    else:
        all_c_files = utils.list_c_files(args.recursive, args.directory)

    start_all = time.time()

    n_func = 0
    pbar = Bar(all_c_files, verbose=args.verbose)
    for c_file in pbar:
        pbar.set_description("Checking %s" % c_file)
        start = time.time()

        n_func += shell.run_esbmc(c_file, cmd_line, dep_list, args)

        elapsed = (time.time() - start)
        log.finish_time(c_file, elapsed)

    elapsed_all = (time.time() - start_all)
    log.overall_time(elapsed_all)
    cex_list = csvwr.search_cex(log_name)
    current, peak = tracemalloc.get_traced_memory()
    log.summary(len(all_c_files), n_func, len(cex_list), elapsed_all, peak)

    csvwr.export_cex(cex_list, log_name)
    print("LSVerifier - Verification is complete.")

if __name__ == "__main__":
    main()
