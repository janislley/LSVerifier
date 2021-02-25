#!/usr/bin/env python3
import os

# store a file content in a list of lines
def code2list(filename):
    lines = []
    file = open(filename, 'r')
    for line in file:
        lines.append(line)
    file.close()
    return lines

# write a list of lines to a file
def list2code(lines, filename):
    file = open(filename, 'w')
    for line in lines:
        file.write(line)
    file.close()

# instrument code with assumes w.r.t. given map
def instrument_code(filename, map):
    print('Instrumenting source-code with given parameters')
    line_numbers = set([line_number for line_number in map])
    lines = code2list(filename)
    instrumented = []
    for idx in range(0, len(lines)):
        if idx + 1 in line_numbers:
            instrumentation = map[idx + 1]
            var_name = instrumentation[0]
            var_value = instrumentation[1]
            spaces = len(lines[idx]) - len(lines[idx].lstrip())
            assume = '__ESBMC_assume({0} == {1});\n'.format(var_name, var_value)
            instrumented.append(' ' * spaces + assume)
        instrumented.append(lines[idx])
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    output_filename = os.path.join(dirname, 'instrumented_' + basename)
    list2code(instrumented, output_filename)
    print('Output file saved in {0}'.format(output_filename))
