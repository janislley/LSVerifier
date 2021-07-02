## esbmc-wr
A [ESBMC](https://github.com/esbmc/esbmc) wrapper thats allow to verify multiples files and functions on a single run.

## Installation
#### Dependecies
You must have ESBMC built and exported on yout PATH variable.  
This [guide](https://github.com/esbmc/esbmc/blob/master/BUILDING.md) describe how build ESBMC.

#### Install esbmc-wr

##### From repo
1. Clone this repo:
```
$ git clone https://github.com/thalestas/esbmc-wr.git
```

2. Install using pip
```
$ cd esbmc-wr 
$ pip3 install .
```

##### From Pypi
```
$ pip3 install esbmc-wr
```

## Usage

###### 1. Verify all ```.c``` files in a folder:  

In the project that you want to verify, run:
```
$ esbmc-wr
```

###### 2. Configure ESBMC parameters:  

To set the ESBMC parameter, you should use ```-e```:
```
$ esbmc-wr -e "--unwind 1 --no-unwinding-assertions"
```

###### 3. esbmc-wr help
```
$ esbmc-wr -h

usage: Input Options [-h] [-e ESBMC_PARAMETER] [-i LIBRARIES] [-f] [-v] [-r] [-d DIRECTORY] [-fl FILE] [-rp]

optional arguments:  
  -h, --help		show this help message and exit  
  -e ESBMC_PARAMETER, --esbmc-parameter ESBMC_PARAMETER  
                        Use ESBMC parameter  
  -i LIBRARIES, --libraries LIBRARIES  
                        Path to the file that describe the libraries dependecies  
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
