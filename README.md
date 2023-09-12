## LSVerifier

An open-source tool that allows to verification of large files and functions on a single run.
This tool uses [ESBMC](https://github.com/esbmc/esbmc) module as a core verification. 

## Version

| Version | Improviments |
|---------|--------------|
| v0.3.0  | Support specific class of property verification; Prioritized functions verification, disable invalid pointer verification. |
| v0.2.0  | Support for libraries dependencies; recursive verification for large software. |

## Installation

#### Install LSVerifier

##### From repo

1. Clone this repository:

```
$ git clone https://github.com/janislley/lsverifier.git
```

2. Than, install using pip

```
$ cd LSVerifier
$ pip3 install .
```

##### From Pypi

```
$ pip3 install lsverifier
```

## Usage

###### 1. Verify a single ```.c``` file:  

In the project that you want to verify, run:

```
$ lsverifier -v -r -f -fp main.c
```
> **_NOTE:_**  ```-v``` is used to enable verbose output; ```-r``` is used to enable recursive verification; 

###### 2. Verify all ```.c``` files in a folder:  

In the project that you want to verify, run:

```
$ lsverifier -v -r -f
```

If the project has libraries dependencies, you should use ```-l``` to set the libraries dependencies file path:

```
$ lsverifier -v -r -f -l dep.txt
```

For exemple of ```dep.txt``` file, see below:

```
  /usr/include/glib-2.0/
  /usr/lib/x86_64-linux-gnu/glib-2.0/include/
  extcap/
  plugins/epan/ethercat/
  plugins/epan/falco_bridge/
  plugins/epan/wimaxmacphy/
  randpkt_core/
  writecap/
  epan/crypt/
```

###### 3. Verify all ```.c``` files in a folder by priorization:  

In the project that you want to verify, run:

```
$ lsverifier -v -r -f -fp
```

###### 4. Verify all ```.c``` files given a list of propertie's name:  

In the project that you want to verify, run:

```
$ lsverifier -v -r -f -p memory-leak-check,overflow-check,deadlock-check,data-races-check
```

###### 5. Configure ESBMC module parameters:  

To set the ESBMC parameter, you should use ```-e```:
```
$ lsverifier -e "--unwind 1"
```

> **_NOTE:_** ```-e``` is used to set the ESBMC module parameters;

###### 6. Verify an entire project folder by passing the folder path as an argument:

To set the folder path parameter, you should use ```-d```:

```
lsverifier -r -f -i dep.txt -d folder_path/
```

###### 7. Verify an entire project folder without checking invalid pointer ```-dp```:

To set the parameter, you should use ```-dp```:

```
lsverifier -r -f -dp -d folder_path/
```

###### 8. LSVerifier help

For more details, please check the help:

```
$ lsverifier -h

usage: lsverifier [-h] [-l LIBRARIES] [-p PROPERTIES] [-f] [-fp] [-fl FILE] [-v] [-r] [-d DIRECTORY] [-dp] [-e ESBMC_PARAMETER]

Input Options

optional arguments:
  -h, --help            show this help message and exit
  -l,--libraries LIBRARIES
                        Path to the file that describes the libraries dependencies
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

## Verification output 

The verification output will be saved on ```output``` folder that will be created on the current verification path.
Each verification will generate two files:

- lsverifier-**DATE**.log: This file contains the verification output log.
- lsverifier-**DATE**.csv: This file contains the verification output in csv format.