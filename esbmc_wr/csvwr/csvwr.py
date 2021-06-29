#!/usr/bin/env python3
import csv
import re
import sys
import os

count = 0
namePattern = 'function(.*)thread'
linePattern = 'line(.*)function'
fileNamePattern = 'FILE](.*)'
funcVeriPattern = 'FUNCTION](.*)'
fileName = ''
funcVeri = ''
functionName = ''
functionLine = ''
errorPattern = 'Violated property'
errorName = ''
DIRECTORY = "output"

def create_csv():
    with open(os.path.join(DIRECTORY,'output.csv'), mode='w') as csv_file:
        fieldnames = ['fileName',
                'functionVerified',
                'functionName',
                'functionLine',
                'error']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
    csv_file.close()

def search_duplicate(file_name, function_name, line):
    with open(os.path.join(DIRECTORY,'output.csv'), mode='r') as csv_file:
        for row in csv.reader(csv_file):
            if(file_name and function_name and line in row):
                csv_file.close()
                return True;

def search_cex():
    hasFailed = False
    cex_list = []
    with open(os.path.join(DIRECTORY, "output.log")) as fp: 
        lines = fp.readlines()
        for i in range(0, len(lines)):
            line = lines[i]

            if('FILE' in line):
                match = re.search(fileNamePattern, line)
                if(match):
                    fileName = match.group(1)

            if('FUNCTION' in line):
                match = re.search(funcVeriPattern, line)
                if(match):
                    funcVeri = match.group(1)

            if('Counterexample' in line):
                hasFailed = True

            if(hasFailed):
                match = False
                functionName = ''
                functionLine = ''
                errorName = ''

                # Find Line
                match = re.search(linePattern, line, re.IGNORECASE)
                if(match):
                    functionLine = match.group(1)

                # Find function name
                match = re.search(namePattern, line, re.IGNORECASE)
                if(match):
                    functionName = match.group(1)

                    # Find error name
                    for j in range(1,6):
                        newLine = lines[i + j]
                        match = re.search(errorPattern, newLine, re.IGNORECASE)
                        if(match):
                            errorName = lines[i + j + 2].rstrip()

                            cex_list.append([fileName, funcVeri, functionName, functionLine, errorName])
    return cex_list

def export_cex():
    create_csv()
    cex_list = search_cex()
    for cex in cex_list:
        if(not search_duplicate(cex[0], cex[2], cex[3])):
            with open(os.path.join(DIRECTORY,'output.csv'), mode='a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(cex)
