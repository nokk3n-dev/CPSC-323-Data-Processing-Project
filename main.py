# Project for Compilers Class
# Written by Dylan Werelius

import re

# Global Constants for the file names (CHANGE THESE FOR YOUR OWN MACHINES)
INPUT_FILE_PATH  = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\Group Project\\input.txt'
LEXICON_FILE_PATH = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\Group Project\\lexicon_table.txt'
COMPILED_FILE_PATH = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\Group Project\\compiled_code.txt'

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

remove_comments_and_whitespace(INPUT_FILE_PATH, COMPILED_FILE_PATH)

print("Violet Evergarden")