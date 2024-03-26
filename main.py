# Project for Compilers Class
# Written by Dylan Werelius

# Main file

import project_functions

# Global Constants for the file names (CHANGE THESE FOR YOUR OWN MACHINES)
INPUT_FILE_PATH  = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\CPSC-323-Data-Processing-Project\\input.txt'
LEXICON_FILE_PATH = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\CPSC-323-Data-Processing-Project\\lexicon_table.txt'
COMPILED_FILE_PATH = 'C:\\Coding\\Fullerton Coding\\Compilers - CPSC 323\\CPSC-323-Data-Processing-Project\\compiled_code.txt'

# Variables
lexicon_table = {
    'keywords':     ([], 0),
    'identifiers':  ([], 0),
    'operators':    ([], 0),
    'separators':   ([], 0),
    'literals':     ([], 0)
}

# Main code
project_functions.remove_comments_and_whitespace(INPUT_FILE_PATH, COMPILED_FILE_PATH)

project_functions.count_separators(COMPILED_FILE_PATH, lexicon_table)
project_functions.count_operators(COMPILED_FILE_PATH, lexicon_table)
project_functions.find_literals(COMPILED_FILE_PATH, lexicon_table)
project_functions.count_identifiers(COMPILED_FILE_PATH, lexicon_table)
project_functions.count_keywords(COMPILED_FILE_PATH, lexicon_table)

project_functions.write_lexicon_table(lexicon_table, LEXICON_FILE_PATH)

