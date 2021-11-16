descr='''Logic table generator
---
Program takes in propositional variables and logical formulae and
generates truth tables for all input states. Created with python3
version 3.7 and supports: implication, biconditional operator and
all default boolean operations.

author:     Chandru Suresh
version:    3.0
since:      05.10.21
last:       13.11.21
'''

import re
import sys
from itertools import product


# enables coloured printing
if sys.platform == 'win32' or sys.platform == 'win64':
    os.system('color')


def err(msg):
    ''' Prints coloured error message to console
    and terminates program. '''
    print('\033[91m[error] ' + msg + '\033[00m')
    quit()

# -------------------------------------------

def ascii_table(header, data):
    ''' Draws ascii table for data provided as 2D
    array of rows. '''

    # calculates independent column widths
    ncols = len(data[0])
    fieldmajor = list(zip(*data))
    col_widths = [max([len(str(cell)) + 6 for cell in fieldmajor[col]]) for col in range(ncols)]

    if header is not None:
        if len(header) != len(data[0]):
            err('Header and record have mismatching widths')
        col_widths = [max(len(str(header[i])) + 6, col_widths[i]) for i in range(ncols)]

    # creates print formats
    record_frmt = '|' + '|'.join(['{:^%i}' % w for w in col_widths]) + '|\n'
    line_break  = '+' + '+'.join(['-'*w for w in col_widths]) + '+\n'

    out = line_break
    
    # prints table header
    if header is not None:
        out += record_frmt.format(*header)
        out += line_break
    
    # prints table body
    for row in data:
        if len(row) != ncols:
            err('Rows/records in table have mismatching widths')
        out += record_frmt.format(*row)
    out += line_break
    print(out)

# -------------------------------------------

sanitize_patterns=(
    # biconditional 
    (r'\! *(\w+|\(.+\))', r' not(\1)'),
    
    # biconditional 
    (r'(\w+|\(.+\)) *<-> *(\w+|\(.+\))', r'(\1)==(\2)'),
    
    # implication
    (r'(\w+|\(.+\)) *-> *(\w+|\(.+\))', r' not(\1)or(\2)'),
    (r'(\w+|\(.+\)) *<- *(\w+|\(.+\))', r'(\1)or not(\2)'),
   
    # exclusive or
    (r'(\w+|\(.+\)) *xor *(\w+|\(.+\))', r'(\1)!=(\2)'),
    
    # nand
    (r'(\w+|\(.+\)) *nand *(\w+|\(.+\))', r' not(\1) or not(\2)'),
    
    # nor
    (r'(\w+|\(.+\)) *nor *(\w+|\(.+\))', r' not(\1) and not(\2)'),
    
    # exclusive nor
    (r'(\w+|\(.+\)) *xnor *(\w+|\(.+\))', r'(\1)==(\2)'),
)


def sanitize_func(propvars, str_func):
    ''' Method sanitizes logical-function input so that python can 
    effectively evaluate it. '''
    
    statement=str_func.strip()

    for pattern, substitute in sanitize_patterns:
        while re.search(pattern, statement) is not None:
            statement = re.sub(pattern, substitute, statement)

    for var in propvars:
        statement = statement.replace(var, '{%s}' % var)

    return statement

# -------------------------------------------

def gen_logic_table(propvars, funcs):
    ''' Sanitizes functions passed in and evaluates and generates
    logic data to be converted into table.'''
    
    states = product([False, True], repeat=len(propvars))

    statements = [sanitize_func(propvars, func) for func in funcs]
   
    logic_table_data = []

    for v in states:                                                                                                                                                            
        v_dict = {arg_name: v[i] for i, arg_name in enumerate(propvars)}                                                                                                               
                                                                                                                                                                                      
        o = []                                                                                                                                                                        
        for s in statements:                                                                                                                                                          
            try:                                                                                                                                                                      
                o.append(int(eval(s.format(**v_dict))))                                                                                                                               
            except (SyntaxError, NameError) as e:                                                                                                                                                       
                err("Could not parse statement: " + s)                                                                                                                                
        
        logic_table_data.append((*v, *o))                                                                                                                                             
                                                                                                                                                                                       
    return logic_table_data  

# -------------------------------------------

def main(args):
    ''' Main method facilitates program. '''
    
    if 'help' in args:
        print(descr)
        quit()

    while True:
        try:
            propvars = list(map(str.strip, input('Enter propositional variables separated by commas e.g: P, Q, R\n').split(',')))
            formulas = list(map(str.strip, input('Enter logical formulas separated by commas e.g: P and Q, Q -> R\n').split(',')))

            if 'exit' in propvars or 'exit' in formulas:
                quit()

            if propvars[0] == '' or formulas[0] == '':
                err('Missing arguments or formulas')
                continue

            ascii_table(propvars + formulas, gen_logic_table(propvars, formulas))
        except KeyboardInterrupt:
            err('Good bye world :(')

            
if __name__ == '__main__':
    ''' Program starts here. '''
    main(sys.argv[1:])


