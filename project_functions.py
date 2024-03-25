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

def count_keywords(input_file, table):
    keywords = set() #list of the keywords that were found 
    keyword_list = {'def':0, 'return':0,}
    with open(input_file, 'r') as f: #opening file 
        in_quotes = False  #checks if it have quotes
        def_count = 0
        return_count = 0
        for line in f: # going through the line  
           for word in keyword_list: #going through the keywords
            match_def= re.search(r'def', line)
            if(match_def):
                print("value of word.key", word)
                keyword_list[word] += 1 #incrementing the dic for key 
                keywords.add(match_def.group())

            match_return = re.search(r'return', line)
            if(match_return):
                return_count += 1
                keywords.add(match_return.group())


    #found_keywords ={key: count for key, count in keywords.items() if count >0} #listing what was found 
    table["keywords"] = (list(keywords), (def_count + return_count)) #updates the table

    f.closed #close the file 

def write_lexicon_table(table, output_file):
    with open(output_file, 'w') as f:
        for key, value in table.items():
            f.write(f'{key:12} ==> {value}\n')
    f.closed

def count_identifiers(input_file,table): 
    identifiers = set()
    count = 0

    with open (input_file, 'r') as file:
        for line in file: #This reads the file line by line
                try:
                    found_identifiers = ast.parse(line) # This adds to the syntax tree and adds
                    for node in ast.walk(found_identifiers): # this walks through the syntax tree
                        if isinstance(node, ast.Name):
                            identifiers.add(node.id)
                            count += 1
                except SyntaxError:
                    pass
      

    table["identifiers"] = (list(identifiers), count)