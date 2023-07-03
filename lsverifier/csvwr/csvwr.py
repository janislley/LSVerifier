#!/usr/bin/env python3
import csv
import re
import sys
import os

count = 0
name_pattern = 'function(.*)thread'
line_pattern = 'line(.*)function'
file_name_pattern = 'FILE](.*)'
func_veri_pattern = 'FUNCTION](.*)'
file_name = ''
func_veri = ''
function_name = ''
function_line = ''
error_pattern = 'Violated property'
error_name = ''
DIRECTORY = "output"

def create_csv(csv_name):
    with open(os.path.join(DIRECTORY,csv_name), mode='w') as csv_file:
        fieldnames = ['file_name',
                'functionVerified',
                'function_name',
                'function_line',
                'error']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
    csv_file.close()

def search_duplicate(file_name, function_name, line, csv_name):
    with open(os.path.join(DIRECTORY, csv_name), mode='r') as csv_file:
        for row in csv.reader(csv_file):
            if(file_name and function_name and line in row):
                csv_file.close()
                return True;

def search_cex(log_name):
    has_failed = False
    cex_list = []
    with open(os.path.join(DIRECTORY, log_name)) as fp:
        lines = fp.readlines()
        for i in range(0, len(lines)):
            line = lines[i]

            if('FILE' in line):
                match = re.search(file_name_pattern, line)
                if(match):
                    file_name = match.group(1)

            if('FUNCTION' in line):
                match = re.search(func_veri_pattern, line)
                if(match):
                    func_veri = match.group(1)

            if('Counterexample' in line):
                has_failed = True

            if(has_failed):
                match = False
                function_name = ''
                function_line = ''
                error_name = ''

                # Find Line
                match = re.search(line_pattern, line, re.IGNORECASE)
                if(match):
                    function_line = match.group(1)

                # Find function name
                match = re.search(name_pattern, line, re.IGNORECASE)
                if(match):
                    function_name = match.group(1)

                    # Find error name
                    for j in range(1,6):
                        newLine = lines[i + j]
                        match = re.search(error_pattern, newLine, re.IGNORECASE)
                        if(match):
                            error_name = lines[i + j + 2].rstrip()

                            cex_list.append([file_name, func_veri, function_name, function_line, error_name])
    return cex_list

def export_cex(cex_list, log_name):
    csv_name = log_name[:-3] + "csv"
    create_csv(csv_name)
    for cex in cex_list:
        if(not search_duplicate(cex[0], cex[2], cex[3], csv_name)):
            with open(os.path.join(DIRECTORY, csv_name), mode='a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(cex)
