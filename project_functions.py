# Project for Compilers Class
# Written by Dylan Werelius

# Functions file

import re

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
        '==': 0,
        '=': 0,
        '++': 0,
        '+': 0,
        '--': 0,
        '-': 0,
        '<<': 0,
        '>>': 0
    }

    with open(input_file, 'r') as file:
        in_quotes = False
        for line in file:
            index = 0
            while index < len(line):
                if line[index] == "\"" or line[index] == "\'":
                    in_quotes = not in_quotes
                    index += 1
                    continue
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

def write_lexicon_table(table, output_file):
    with open(output_file, 'w') as f:
        for key, value in table.items():
            f.write(f'{key:12} ==> {value}\n')
    f.closed

def count_identifiers(input_file,table): 
    identifiers = {
        'add': 0,
        'a' : 0,
        'b' : 0,
        'result' : 0,
        'num1' : 0,
        'num2' : 0,
    }

    with open(input_file, 'r') as fle:
        in_quotes = False
        for line in fle:
            index = 0
            while index < len(line):
                    if line[index] == "\"" or line[index] == "\'":
                        in_quotes = not in_quotes
                        index += 1
                        continue
                    elif not in_quotes and line[index] in identifiers:
                        if index + 1 < len(line) and line[index + 1] == line[index]:
                            identifiers[line[index] * 2] += 1
                            index += 2
                            continue
                        identifiers[line[index]] += 1
                    index += 1    
                    
    # Filter out identifiers that are not found
    found_identifiers = {key: count for key, count in identifiers.items() if count > 0}  

    table["identifiers"] = (list(found_identifiers.keys()), sum(found_identifiers.values()))