import time
import argparse
import os
import tracemalloc
from lsverifier.csvwr import csvwr
from lsverifier.log import log
from lsverifier.bar import Bar
from lsverifier.utils import utils
from lsverifier.utils import shell

class colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

class NewLineHelpFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('Properties to be verified'):
            properties = text.replace('Properties to be verified (comma separated): ', '').split(',')
            lines = [prop.strip() for prop in properties]
            return lines
        return argparse.HelpFormatter._split_lines(self, text, width)

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super(NewLineHelpFormatter, self)._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings).replace(', ', ',') + ' ' + args_string

def arguments():

    valid_choices = [
        'multi-property',
        'nan-check',
        'memory-leak-check',
        'floatbv',
        'overflow-check',
        'unsigned-overflow-check',
        'ub-shift-check',
        'struct-fields-check',
        'deadlock-check',
        'data-races-check',
        'lock-order-check'
    ]
        
    parser = argparse.ArgumentParser(description="Input Options", formatter_class=NewLineHelpFormatter)
    parser.add_argument("-l", "--libraries", help="Path to the file that describes the libraries dependencies", default=False)
    parser.add_argument("-p", "--properties", 
                        help="Properties to be verified (comma separated):\n" + 
                             "                        multi-property,\n" + 
                             "  nan-check,\n" + 
                             "  memory-leak-check,\n" +
                             "  floatbv,\n" + 
                             "  overflow-check,\n" + 
                             "  unsigned-overflow-check,\n" +
                             "  ub-shift-check,\n" + 
                             "  struct-fields-check,\n" + 
                             "  deadlock-check,\n" +
                             "  data-races-check,\n" + 
                             "  lock-order-check",
                        metavar="PROPERTIES",
                        default="",
                        type=str)
    parser.add_argument("-f", "--functions", help="Enable Functions Verification", action="store_true", default=False)
    parser.add_argument("-fp", "--function-prioritized", help="Enable Prioritized Functions Verification", action="store_true", default=False)
    parser.add_argument("-fl", "--file", help="File to be verified", default=False)
    parser.add_argument("-v", "--verbose", help="Enable Verbose Output", action="store_true", default=False)
    parser.add_argument("-r", "--recursive", help="Enable Recursive Verification", action="store_true", default=False)
    parser.add_argument("-d", "--directory", help="Set the directory to be verified", default=False)
    parser.add_argument("-dp", "--disable-pointer-check", help="Disable invalid pointer verification", action="store_true", default=False)
    parser.add_argument("-e", "--esbmc-parameter", help="Use ESBMC parameter")

    args = parser.parse_args()

    if args.properties:
        args.properties = [p.strip() for p in args.properties.split(',')]  # This will remove any extra spaces
        for prop in args.properties:
            if prop not in valid_choices:
                print(f"Error: {prop} is not a valid choice.")
                exit(1)

    return(args)

def main():

    tracemalloc.start()

    args = arguments()
    print("[LSVerifier] Loading configuration settings")

    log_name = log.configure(args.verbose)

    # Check if both -f and -fp are given
    if args.functions and args.function_prioritized:
        print(colors.RED + "[LSVerifier] Error: Conflicting options -f and -fp used together" + colors.RESET)
        return 1  # exit with an error code

    cmd_line = utils.get_command_line(args)

    if args.libraries:
        log.info("Dependency files: %s" % args.libraries)
        
        # Create the full path to dep.txt within the specified directory
        dep_txt_path = os.path.join(args.directory, args.libraries) if args.directory else args.libraries
        
        # Check if the file exists in the specified directory
        if os.path.exists(dep_txt_path):
            dep_list = utils.read_dep_file(dep_txt_path)
        else:
            print(f"The file {dep_txt_path} does not exist.")
            dep_list = []
    else:
        dep_list = []

    if args.file:
        all_c_files = [args.file]
    else:
        all_c_files = utils.list_c_files(args.recursive, args.directory)

    start_all = time.time()

    print("[LSVerifier] Running ESBMC model checker")
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
    print(colors.GREEN + "[LSVerifier] Verification completed" + colors.RESET)

if __name__ == "__main__":
    main()
