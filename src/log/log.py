import os
import logging

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

    file_handler = logging.FileHandler("output/output.log")
    logger.addHandler(file_handler)

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

def header_reteste(c_file, esbmc_args, item):
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
