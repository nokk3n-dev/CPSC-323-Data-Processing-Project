# Project for Compilers Class

# Functions file

import re
import ast
import keyword


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
    keywords = [] #list of the keywords that were found 
    with open(input_file, 'r') as f: #opening file
        
        #read the file
        text = f.read()

        #captures the words
        words = re.findall(r'(\'[^\']+\'|\"[^\"]+\"|\b\w+\b)', text)

        #count of keywords found 
        final_count=0
        for word in words: #going through the line as it is split()
            if word[0] in ['\"', '\''] and word[len(word)-1] in ['\"', '\'']:
                pass
            else:
                if word in ["print", "input"] or keyword.iskeyword(word): #if the word is a keyword enter 
                    if (word not in keywords):
                        keywords.append(word) #update the list of keywords found 
                    final_count+=1  #increment the count when the keyword is found

    table["keywords"] = (list(keywords), (final_count)) #updates the table

    f.closed #close the file 

def write_output(table, output_file, test_no, compiled_code_file):

    # Get the compiled code
    with open(compiled_code_file, 'r') as file:
        file_content = file.read()
    file.closed
        
    with open(output_file, 'a') as f:

        # Write the test number
        if test_no > 1:
            f.write(f"\n\n\nTest Number: {test_no}\n\n")
        else:
            f.write(f"Test Number: {test_no}\n\n")

        # Write the copmiled code
        f.write("Code with excess space and comments removed:\n")
        f.write("---------------------------------------------------------------------\n")
        f.write(file_content)
        f.write("---------------------------------------------------------------------\n")

        # Write the table
        f.write("\nTokenized Code:\n")
        f.write("---------------------------------------------------------------------\n")
        for key, value in table.items():
            
            f.write(f'{key:12} ==> {value}\n')
        f.write("---------------------------------------------------------------------\n")
    f.closed

def count_identifiers(input_file,table): 
    identifiers = []
    count = 0

    with open(input_file, 'r') as file:
        try:
            file_content = file.read()
            found_identifiers = ast.parse(file_content) # This adds to the syntax tree and adds
            for node in ast.walk(found_identifiers): # this walks through the syntax tree
                if isinstance(node, ast.Name) and node.id not in ["print", "input"]:
                    if node.id not in identifiers:
                        identifiers.append(node.id)
                    count += 1

                # Case for if it is a function definition
                elif isinstance(node, ast.FunctionDef):
                    if node.name not in identifiers:
                        identifiers.append(node.name)
                    count += 1

                    # Add the function parameters
                    for arg in node.args.args:
                        if arg.arg not in identifiers:
                            identifiers.append(arg.arg)
                        count += 1
        except SyntaxError:
            pass
      

    table["identifiers"] = (list(identifiers), count)

def find_literals(input_file, table):
    # Array to hold the literals that we find
    literals = []
    count = 0

    with open(input_file, 'r') as file:
        for line in file:
            if '\"__main__\"' in line and '\"__main__\"' not in literals:
                count += 1
                literals.append("__main__")
            # Parse the line and extract literals
            try:
                tree = ast.parse(line)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Constant):
                        count += 1
                        # Handle when the node is a string literal
                        if isinstance(node.value, str):
                            # Append the unescaped string literal
                            if node.value not in literals:
                                literals.append(ast.literal_eval(repr(node.value)))
                        else:
                            if node.value not in literals:
                                literals.append(node.value)

            except SyntaxError:
                # Skip the lines with syntax error
                pass
    table["literals"] = (list(literals), count)