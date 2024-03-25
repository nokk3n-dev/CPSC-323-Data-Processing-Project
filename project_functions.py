# Project for Compilers Class
# Written by Dylan Werelius

# Functions file

import re
import ast

def remove_comments_and_whitespace(input_file, output_file):
    with open(input_file, 'r') as f:
        python_code = f.readlines()

    # Regular expression to match Python comments
    pattern = r'#.*?$|\'\'\'.*?\'\'\'|\"\"\".*?\"\"\"'

    with open(output_file, 'w') as f:
        for line in python_code:

            # Remove comments by splitting at the first occurrence of '#'
            line_without_comment = line.split('#', 1)[0]

            # Remove the tabs in front of the lines of code
            line_without_whitespace = line_without_comment.lstrip()

            # Remove the extra white spaces in the lines of code
            line_without_extra_spaces = re.sub(r'\s+', ' ', line_without_whitespace)

            if line_without_extra_spaces.strip():  
                # Write the line with a return at the end because that was being removed too for some reason
                f.write(line_without_extra_spaces.strip()  + '\n')
        
    f.closed

# This currents does not handle \' or \" yet
def count_separators(input_file, table):
    separators = {
        ',': 0,
        ';': 0,
        ':': 0,
        '(': 0,
        ')': 0,
        '[': 0,
        ']': 0,
        '{': 0,
        '}': 0
    }

    with open(input_file, 'r') as f:
        in_quotes = False
        for line in f:
            for char in line:
                if char == "\"" or char == "\'":
                    in_quotes = not in_quotes  # Toggle the in_quotes flag
                elif not in_quotes and char in separators:
                    separators[char] += 1

    found_separators = {key: count for key, count in separators.items() if count > 0}
    
    table["separators"] = (list(found_separators.keys()), sum(found_separators.values()))

    f.closed

def count_operators(input_file, table):
    operators = {
        '==':   0,
        '=':    0,
        '++':   0,
        '+':    0,
        '--':   0,
        '-':    0,
        '<<':   0,
        '>>':   0
    }

    with open(input_file, 'r') as file:
        # This variable will keep track of if we are starting or ending quotes
        in_quotes = False
        for line in file:
            # Index represents each character in the line
            index = 0
            
            # Loop for the length of the line, checking every character
            while index < len(line):

                # Logic to determine if we encounter a quote
                if line[index] == "\"" or line[index] == "\'":
                    in_quotes = not in_quotes
                    index += 1
                    continue
                # Logic for finding the operators that are not in quotes
                elif not in_quotes and line[index] in operators:
                    if index + 1 < len(line) and line[index + 1] == line[index]:
                        operators[line[index] * 2] += 1
                        index += 2  # Move to the next character after the second consecutive operator
                        continue
                    operators[line[index]] += 1
                index += 1

    # Filter out operators that were not found
    found_operators = {key: count for key, count in operators.items() if count > 0}

    table["operators"] = (list(found_operators.keys()), sum(found_operators.values()))

def find_literals(input_file, table):
    # Array to hold the literals that we find
    literals = []

    with open(input_file, 'r') as file:
        for line in file:
            # Parse the line and extract literals
            try:
                tree = ast.parse(line)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Constant):
                        # Handle when the node is a string literal
                        if isinstance(node.value, str):
                            # Append the unescaped string literal
                            literals.append(ast.literal_eval(repr(node.value)))
                        else:
                            literals.append(node.value)

            except SyntaxError:
                # Skip the lines with syntax error
                pass
    table["literals"] = (list(literals), len(literals))

def write_lexicon_table(table, output_file):
    with open(output_file, 'w') as f:
        for key, value in table.items():
            f.write(f'{key:12} ==> {value}\n')
    f.closed