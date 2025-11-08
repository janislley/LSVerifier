import os
import sys
import subprocess
import glob
from pathlib import Path
from shutil import which
from pathlib import Path
from lsverifier.log import log

ESBMC = "esbmc"
CTAGS = "ctags"
CTAGS_TAB = "-x"
CTAGS_FUNC = "--c-types=f"
DEFAULT_ESBMC_OPTIONS = "--unwind 1 --no-unwinding-assertions"

def ensure_compdb(project_dir, build_dir="build"):
    """
    Find or generate compile_commands.json for project_dir.

    Tries in order:
      1) <project_dir>/compile_commands.json
      2) <project_dir>/<build_dir>/compile_commands.json
      3) If CMakeLists.txt exists: cmake -S . -B <build_dir> -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
      4) If Makefile exists and 'bear' available: bear -- make -j  (writes to project root)

    Returns absolute path to compile_commands.json or None.
    """
    project_dir = os.path.abspath(project_dir)
    cand1 = os.path.join(project_dir, "compile_commands.json")
    if os.path.exists(cand1):
        return cand1

    cand2 = os.path.join(project_dir, build_dir, "compile_commands.json")
    if os.path.exists(cand2):
        return cand2

    # Try CMake
    cmakelists = os.path.join(project_dir, "CMakeLists.txt")
    if os.path.exists(cmakelists) and which("cmake"):
        bd = os.path.join(project_dir, build_dir)
        os.makedirs(bd, exist_ok=True)
        log.info(f"[compdb] Generating with CMake in {bd}")
        try:
            subprocess.check_call(
                ["cmake", "-S", project_dir, "-B", bd, "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"],
                cwd=project_dir
            )
            cand = os.path.join(bd, "compile_commands.json")
            if os.path.exists(cand):
                return cand
        except subprocess.CalledProcessError:
            log.warn("[compdb] CMake failed to configure; will try other methods")

    # Try Bear over Make
    makefile = os.path.join(project_dir, "Makefile")
    if os.path.exists(makefile) and which("bear"):
        log.info("[compdb] Generating with Bear over make")
        try:
            subprocess.check_call(["bear", "--", "make", "-j"], cwd=project_dir)
            cand = os.path.join(project_dir, "compile_commands.json")
            if os.path.exists(cand):
                return cand
        except subprocess.CalledProcessError:
            log.warn("[compdb] Bear failed to generate compile_commands.json")

    return None

def get_command_line(args):

    cmd_line = ""

    # Start with the default ESBMC options
    if not args.esbmc_parameter:
        cmd_line = DEFAULT_ESBMC_OPTIONS
    else:
    # If the user has specified custom ESBMC parameters, use them
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

    search_path = directory if directory else "."

    if recursive:
        for path in Path(search_path).rglob("*.c"):
            file_list.append(str(path))
    elif directory:
        file_list = glob.glob(os.path.join(search_path, "*.c"))
    else:
        file_list = glob.glob("*.c")

    if not len(file_list):
        log.error("There is not .c file here!")
        sys.exit()

    return(file_list)

def is_esbmc_installed():
    if not which(ESBMC) is not None:
        print("ESBMC module not found!")
        sys.exit()
