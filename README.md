# LSVerifier

[![PyPI version](https://img.shields.io/pypi/v/lsverifier.svg)](https://pypi.org/project/lsverifier/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)

LSVerifier is a command-line tool for formal verification of large ANSI-C projects in a single run. 

It leverages the [ESBMC](https://github.com/esbmc/esbmc) model checker as its core verification engine.

Demo [video](https://www.youtube.com/watch?v=LrGwp00pSLc).

## Architecture Overview

The diagram below summarizes the LSVerifier verification workflow:

![LSVerifier Architecture](https://github.com/janislley/LSVerifier/blob/main/lsverifier/docs/lsverifier_architecture.png)

**Workflow Steps:**

1. **Input**: Project source code (C files).
2. **Preprocessing**: Parses function listings and configures library dependencies (if any).
3. **Function Prioritization** *(optional)*: Orders verification by risk/importance.
4. **Model Checking**: Each function is analyzed via **ESBMC**.
5. **Result Generation**: Logs and reports verification outcomes.

## Version

| Version | Improvements |
|---------|--------------|
| v0.4.0  | Support ESBMC v7.10, improved symbolic modeling of thread-local globals and data race detection, and introduced support for termination analysis to detect non-terminating loops in C programs. |
| v0.3.0  | Support specific class of property verification; Support for large software; Prioritized functions verification, Disable invalid pointer verification. |
| v0.2.0  | Support for libraries dependencies; Recursive verification. |

## Requirements

[Ctags](https://github.com/universal-ctags/ctags) is required to use LSVerifier.

## Installation

#### Install LSVerifier

##### From repository

1. Clone the repository:

```
$ git clone https://github.com/janislley/lsverifier.git
```

2. Install using pip:

```
$ cd LSVerifier
$ pip3 install .
```

##### From Pypi

```
$ pip3 install lsverifier
```

## Usage

#### 1. Verify a project
```
$ cd <project-root>
$ lsverifier -r -f
```

For projects with third-party library dependencies, use ```-l``` option to specify header paths:

```
$ lsverifier -r -f -l dep.txt
```

See an example of ```dep.txt``` below:

```
  /usr/include/glib-2.0/
  /usr/lib/x86_64-linux-gnu/glib-2.0/include/extcap/
  extcap/
  plugins/epan/ethercat/
  plugins/epan/falco_bridge/
  plugins/epan/wimaxmacphy/
  epan/crypt/
  ...
```

#### 2. Verify a single C file

```
$ lsverifier -f -fl file.c
```

#### 3. Verify C files using a priorization algorithm

If you want to verify a project using a prioritization scheme, run:

```
$ cd <project-root>
$ lsverifier -r -fp
```

#### 4. Verify an entire project by providing the folder path as an argument

To set the folder path parameter, you should use ```-d```:

```
lsverifier -r -f -l dep.txt -d project-root/
```

#### 5. Verify C files using a predefined class of properties

In the project that you want to verify, run:

```
$ lsverifier -r -f -p memory-leak-check,overflow-check,deadlock-check,data-races-check
```

See more properties on tool help.

#### 6. LSVerifier help

For more details, check the help:

```
$ lsverifier -h

usage: lsverifier [-h] [-l LIBRARIES] [-p PROPERTIES] [-f] [-fp] [-fl FILE] [-v] [-r] [-d DIRECTORY] [-dp] [-e ESBMC_PARAMETER]

Input Options

optional arguments:
  -h, --help            show this help message and exit
  -l,--libraries LIBRARIES
                        Path to the file that describes the libraries' dependencies
  -p,--properties PROPERTIES
                        Properties to be verified (comma separated):
                        multi-property
                        nan-check
                        memory-leak-check
                        floatbv
                        overflow-check
                        unsigned-overflow-check
                        ub-shift-check
                        struct-fields-check
                        deadlock-check
                        data-races-check
                        lock-order-check
  -f, --functions       Enable Functions Verification
  -fp, --function-prioritized
                        Enable Prioritized Functions Verification
  -fl,--file FILE       File to be verified
  -v, --verbose         Enable Verbose Output
  -r, --recursive       Enable Recursive Verification
  -d,--directory DIRECTORY
                        Set the directory to be verified
  -dp, --disable-pointer-check
                        Disable invalid pointer property verification
  -e,--esbmc-parameter ESBMC_PARAMETER
                        Use ESBMC parameter
```

## Verification report

The verification results will be saved in ```output``` folder, automatically created in the current verification path. Each verification run generates two files:

- lsverifier-**DATE**.log: Contains the verification output log.
- lsverifier-**DATE**.csv: Contains the verification results in CSV format.
