# Project for Compilers Class
# Written by Dylan Werelius

# Main file

import project_functions

# Global Constants for the file names (CHANGE THESE FOR YOUR OWN MACHINES)
INPUT_FILE_PATH  = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\CPSC-323-Data-Processing-Project\\input.txt'
OUTPUT_FILE_PATH = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\CPSC-323-Data-Processing-Project\\output.txt'
COMPILED_FILE_PATH = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\CPSC-323-Data-Processing-Project\\compiled_code.txt'

# Constants for the second test
INPUT_FILE_PATH_2 = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\CPSC-323-Data-Processing-Project\\input 2.txt'
COMPILED_FILE_PATH_2 = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\CPSC-323-Data-Processing-Project\\compiled_code 2.txt'


# Variables
lexicon_table = {
    'keywords':     ([], 0),
    'identifiers':  ([], 0),
    'operators':    ([], 0),
    'separators':   ([], 0),
    'literals':     ([], 0)
}

# Main code

# Clear the output file
with open(OUTPUT_FILE_PATH, 'w'):
    pass

# Test Number 1
project_functions.remove_comments_and_whitespace(INPUT_FILE_PATH, COMPILED_FILE_PATH)
project_functions.count_identifiers(INPUT_FILE_PATH, lexicon_table)
project_functions.count_separators(COMPILED_FILE_PATH, lexicon_table)
project_functions.count_operators(COMPILED_FILE_PATH, lexicon_table)
project_functions.count_keywords(COMPILED_FILE_PATH, lexicon_table)
project_functions.find_literals(COMPILED_FILE_PATH, lexicon_table)
project_functions.write_output(lexicon_table, OUTPUT_FILE_PATH, 1, COMPILED_FILE_PATH)

#Test Number 2
project_functions.remove_comments_and_whitespace(INPUT_FILE_PATH_2, COMPILED_FILE_PATH_2)
project_functions.count_identifiers(INPUT_FILE_PATH_2, lexicon_table)
project_functions.count_separators(COMPILED_FILE_PATH_2, lexicon_table)
project_functions.count_operators(COMPILED_FILE_PATH_2, lexicon_table)
project_functions.count_keywords(COMPILED_FILE_PATH_2, lexicon_table)
project_functions.find_literals(COMPILED_FILE_PATH_2, lexicon_table)
project_functions.write_output(lexicon_table, OUTPUT_FILE_PATH, 2, COMPILED_FILE_PATH_2)