**-- This tool is still under development! --**

## esbmc-wr
A [ESBMC](https://github.com/esbmc/esbmc) wrapper thats allow to verify multiples files and functions on a single run.

## Installation
#### Dependecies
You must have ESBMC built and exported on yout PATH variable.  
This [guide](https://github.com/esbmc/esbmc/blob/master/BUILDING.md) describe how build ESBMC.

#### Install esbmc-wr
1. Clone this repo:
```
$ git clone https://github.com/thalestas/esbmc-wr.git
```

2. Install using pip
```
$ cd esbmc-wr 
$ pip3 install .
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

