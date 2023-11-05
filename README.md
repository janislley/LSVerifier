## LSVerifier

LSVerifier is a command-line tool for formal verification of large ANSI-C projects in a single run. 

It leverages the [ESBMC](https://github.com/esbmc/esbmc) model checker as its core verification engine.

Demo [video](https://www.youtube.com/watch?v=LrGwp00pSLc).

## Version

| Version | Improviments |
|---------|--------------|
| v0.3.0  | Support specific class of property verification; Support for large software; Prioritized functions verification, Disable invalid pointer verification. |
| v0.2.0  | Support for libraries dependencies; Recursive verification. |

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
