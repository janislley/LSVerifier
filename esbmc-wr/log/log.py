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
