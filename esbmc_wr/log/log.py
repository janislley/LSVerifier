import os
import sys
import logging
from datetime import datetime

DIRECTORY = "output"
LOG_FILE = "output.log"

def create_dir(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print("Directory ", name, " already exists.")

def configure(verbose):
    create_dir(DIRECTORY)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if verbose:
        stdout_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stdout_handler)

    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    log_name = "esbmc-{}.log".format(date)

    file_handler = logging.FileHandler("output/"+log_name)
    logger.addHandler(file_handler)

    return log_name

def info(msg):
    logging.info(msg)

def error(msg):
    logging.info(msg)

def header(c_file, esbmc_args, item):
    logging.info("########################################")
    logging.info("[FILE] %s", c_file)
    logging.info("[ARGS] %s", esbmc_args)
    logging.info("[FUNCTION] %s", item)
    logging.info("########################################\n")

def header_retest(c_file, esbmc_args, item):
    logging.info("")
    logging.info("########################################")
    logging.info("*****RETEST*****")
    logging.info("[FILE] %s", c_file)
    logging.info("[ARGS] %s", esbmc_args)
    logging.info("[FUNCTION] %s", item)
    logging.info("########################################\n")

def finish_time(c_file, elapsed):
    logging.info("########################################")
    logging.info("[FILE]: %s [TIME]: %s", c_file, elapsed)
    logging.info("########################################\n")

def overall_time(elapsed_all):
    logging.info("[OVERALL TIME]: %s", elapsed_all)

def summary(n_files, n_func, n_cex, time, memory):
    print("\n########################################")
    print("Summary:\n")
    print("Files Verified: ", n_files)
    print("Functions Verified: ", n_func)
    print("Counterexamples: ", n_cex)
    print("")
    print(f"Overall time: {round(time,2)}s")
    print(f"Peak Memory Usage: {round((memory / 10**6),2)}MB")
    print("########################################\n")

