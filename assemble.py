r"""
     _____   _____ _____
    | _ \ \ / / __|__ / |__
    |  _/\ V / (__ |_ \ '_ \
    |_|   |_| \___|___/_.__/
    Python LC3b Assembler

Usage : python assemble.py source [output] [-flags]

Arguments
---------
source
    Source LC3b assembly file
output
    Optional output file; defaults to the same name as source, except with
    a .obj extension

Flags
-----
-p
    Print out assembled files
-t
    Print out symbol table
"""

import os
from print import *

from src import Program


__HEADER = render(r"""
     _____   _____ _____
    | _ \ \ / / __|__ / |__
    |  _/\ V / (__ |_ \ '_ \
    |_|   |_| \___|___/_.__/
    Python LC3b Assembler

""", BR + RED, BOLD)

__HINT = """Usage : python assemble.py source [output] [-flags]

Arguments
---------
source
    Source LC3b assembly file
output
    Optional output file; defaults to the same name as source, except with
    a .obj extension

Flags
-----
-p
    Print out assembled files
-t
    Print out symbol table

"""


if __name__ == "__main__":

    import sys

    print(__HEADER)

    # Parse args
    flags = ([i for i in sys.argv[1:] if i[0] == '-'] + [''])[0]
    args = [i for i in sys.argv[1:] if i[0] != '-']

    if len(args) == 1:
        tgt = args[0]
        save = os.path.basename(args[0]).split('.')[0] + '.obj'
    elif len(args) == 2:
        tgt = args[0]
        save = args[1]
    else:
        print(__HINT)
        exit(1)

    # Assemble program
    p = Program(tgt).assemble()

    # Print info
    if 't' in flags:
        p.print_symbols()
    if 'p' in flags:
        p.print_program()

    p.summary()

    # Save and exit
    if p.is_errored():
        exit(1)
    else:
        p.save_output(save)
        exit(0)
