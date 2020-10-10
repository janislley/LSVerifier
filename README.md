**-- This tool is still under development! --**

### Prepare the environment

Make the script executable
```
chmod +x esbmc-wr.py
```

Export the script path
```
export PATH=$PATH:$PWD
```

### Run the script

In order to run the esbmc-wr, it is necessary run it on the folder where .c files are located.

Following parameter could be used:

`-m` - Enable Memory Leak Check;  
`-u` - Enable and set unwind number. Ex. `-u 50`;  
`-nu` - Enable No Unwind Assertions;  
`-ib` - Enable Incremental BMC;  
`-p` - Enable No Pointer Check;  
`-o` - Enable Overflow Check;  
`-k` - Enable k-induction parallel;  
`-i` - "Path to the file that describe the libraries dependecies. Each line must contain a library dependency path. Refer to a `dep.txt` as example". Ex `-i dep.txt`;  
`-t` - Enable ESBMC timeout in second;  
`-f` - Enable Verification by function;  
`-w` - Enable Witness Output. It makes ESBMC generate graphML;  
`-h` - Shows help;  

An usage example:
```
python3 esbmc-wr.py -u 1 -nu -i dep.txt
```
