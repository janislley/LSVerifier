## LSVerifier

An open-source tool that allows to verification of large files and functions on a single run.
This wrapper uses [ESBMC](https://github.com/esbmc/esbmc) module as a core verification. 

## Installation
#### Install LSVerifier

##### From repo
1. Clone this repo:
```
$ git clone https://github.com/janislley/lsverifier.git
```

2. Install using pip
```
$ cd lsverifier
$ pip3 install .
```

##### From Pypi
```
$ pip3 install lsverifier
```

## Usage

###### 1. Verify all ```.c``` files in a folder:  

In the project that you want to verify, run:
```
$ lsverifier
```

###### 2. Configure ESBMC parameters:  

To set the ESBMC parameter, you should use ```-e```:
```
$ lsverifier -e "--unwind 1 --no-unwinding-assertions"
```

###### 3. Verify each function of ```.c``` files recursively:  

To set the ESBMC parameter, you should use ```-e```:
```
$ lsverifier -r -f -e "--unwind 1 --no-unwinding-assertions"
```

###### 4. Verify an entire project folder by passing the folder path as an argument:

To set the folder path parameter, you should use ```-d```:
```
lsverifier -r -f -e "--unwind 1 --no-unwinding-assertions" -i dep.txt -d folder_path/
```

###### 5. LSVerifier help

```
$ lsverifier -h

usage: Input Options [-h] [-e ESBMC_PARAMETER] [-i LIBRARIES] [-f] [-v] [-r] [-d DIRECTORY] [-fl FILE] [-rp]

optional arguments:  
  -h, --help		show this help message and exit  
  -e ESBMC_PARAMETER, --esbmc-parameter ESBMC_PARAMETER  
                        Use ESBMC parameter  
  -i LIBRARIES, --libraries LIBRARIES  
                        Path to the file that describes the libraries dependencies  
  -f, --functions       Enable Functions Verification  
  -v, --verbose         Enable Verbose Output  
  -r, --recursive       Enable Recursive Verification  
  -d DIRECTORY, --directory DIRECTORY  
                        Set the directory to be verified  
  -fl FILE, --file FILE  
                        File to be verified  
  -rp, --retest-pointer  
                        Retest Invalid Pointer
```

## Verification output 

The verification output will be saved on ```output``` folder that will be created on the current path.
Each verification will generate two files:

- lsverifier-**DATE**.log
- lsverifier-**DATE**.csv
