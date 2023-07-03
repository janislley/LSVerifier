import re

def parse_functions(filename):
    functions_list = []

    # Read C file
    with open(filename, 'r') as file:
        # Initial state
        state = "GET_NAME_AND_PARAMS"
        last_state = ""
        function_name = ""
        parameters = ""
        body = ""
        open_brackets_count = 0

        # Process each line
        for line in file:
            # Remove leading white spaces
            line = line.lstrip()

            # Remove commented parts from line (/*...*/)
            line = re.sub(r"/\*.*?\*/", "", line)

            # If the line is not empty
            if line:
                if state == "GET_NAME_AND_PARAMS":
                    # Ignore commented and "#include" lines
                    if line.startswith("//") or line.startswith("#include"):
                        continue

                     # Handle block comments
                    elif line.startswith("/*"):
                        state = "BLOCK_COMMENT"
                        last_state = "GET_NAME_AND_PARAMS"
                        continue

                    # Handle function start
                    elif "{" in line:
                        body += "{\n"
                        state = "GET_BODY"
                        open_brackets_count = 1

                    # Extract function name and parameters list
                    if not function_name or not parameters:
                        pattern = r'^\s*(\w+(?:\s*\*+)?)\s+(\w+)\((.*?)\)'
                        match = re.match(pattern, line)
                        if match:
                            function_name = match.group(2)
                            parameters = match.group(3)

                # State for jumping block comments
                elif state == "BLOCK_COMMENT":
                    # Continue in the same state until finding the end of the block comment
                    if "*/" in line:
                        state = last_state

                # Handle function body
                elif state == "GET_BODY":
                    # Ignore commented lines
                    if line.startswith("//"):
                        continue
                    # Ignore block comments
                    if line.startswith("/*"):
                        state = "BLOCK_COMMENT"
                        last_state = "GET_BODY"
                        continue

                    body += line

                    # Process function
                    if "}" in line:
                      open_brackets_count -= 1
                      # End of the function
                      if open_brackets_count == 0:
                        functions_list.append((function_name, parameters, body))
                        function_name = ""
                        parameters = ""
                        body = ""
                        state = "GET_NAME_AND_PARAMS"
                    # Handle curly brackets
                    elif "{" in line:
                        open_brackets_count += 1

    return functions_list

def get_prioritized_functions(filename):
    function_dict = {}
    called_functions = set()

    functions = parse_functions(filename)

    # Process function declarations and bodies
    for func_name, parameters, body in functions:
        function_dict[func_name] = {
            'priority': 0, # Initialize priority to 0
        }

        # Update priorities based on parameter types
        if '*' in parameters:  # Function contains pointers as parameters
            function_dict[func_name]['priority'] = 5
        elif '[]' in parameters:  # Function contains vectors as parameters
            function_dict[func_name]['priority'] = 4

        # Search for dynamic memory allocation functions (malloc and free)
        if 'malloc(' in body or 'free(' in body:
            function_dict[func_name]['priority'] = max(function_dict[func_name]['priority'], 3)

        # Search for pthread functions (pthread_create and pthread_join)
        if 'pthread_create(' in body or 'pthread_join(' in body:
            function_dict[func_name]['priority'] = max(function_dict[func_name]['priority'], 2)

        # Search for bit shift and division operations
        if '<<' in body or '>>' in body or '/' in body:
            function_dict[func_name]['priority'] = max(function_dict[func_name]['priority'], 1)

        # Find called functions within the body
        called_functions.update(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', body))

    # Exclude called functions from the prioritized list
    for func_name in called_functions:
        if func_name in function_dict:
            del function_dict[func_name]

    # Sort the function list based on priorities
    sorted_functions = sorted(function_dict.keys(), key=lambda x: (-function_dict[x]['priority'], x))

    return sorted_functions
