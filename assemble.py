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

from exceptions import *
from instruction import Instruction


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


class Program:
    """LC3b Assembly Program

    Parameters
    ----------
    file : str
        File to assemble
    """

    def __init__(self, file):

        self.target = file
        with open(file) as f:
            lines = f.readlines()
            f.close()

        self.symbol_table = {}

        self.maxwidth = max(len(i) for i in lines)
        self.__div = (
            "+------+--------+--------+-{d}-+"
            .format(d='-' * self.maxwidth))
        self.instructions = [
            Instruction(
                i,
                table=self.symbol_table,
                maxwidth=self.maxwidth,
                linenum=idx)
            for idx, i in enumerate(lines)]

    def assemble(self):
        """Assemble instructions

        Returns
        -------
        self
            Allow method chaining
        """

        # First pass
        addr = None
        for i in self.instructions:
            addr = i.assign(addr)

        # Second pass
        for i in self.instructions:
            i.assemble()

        return self

    def print_symbols(self):
        """Print symbol table"""

        print("Symbol Table")
        table.table(
            [["Symbol", "Address"]] + [
                [key, "0x{:04X}".format(value)]
                for key, value in self.symbol_table.items()
            ])
        print("\n")

    def print_program(self):
        """Print assembled program"""
        print(
            "Assembled Program\n"
            "{div}\n"
            "| Line |  Addr  |  Code  |  Source {p} | Errors\n"
            "{div}\n"
            "{code}\n"
            "{div}\n\n"
            .format(
                p=' ' * (self.maxwidth - 8),
                div=self.__div,
                code="\n".join(str(i) for i in self.instructions)))

    def save_output(self, file):
        """Save output to file

        Parameters
        ----------
        file : str
            Output file
        """
        with open(file, "w") as out:
            for i in self.instructions:
                if i.assembled is not None:
                    out.write("0x{:04X}\n".format(i.assembled))
        print(
            "Saved output to {tgt}."
            .format(tgt=os.path.basename(file)), BR + GREEN)

    def is_errored(self):
        """Check if program contains an error"""

        for i in self.instructions:
            if len(i.err) > 0:
                return True
        return False

    def summary(self):
        """Print summary statistics"""

        errored = [i for i in self.instructions if len(i.err) > 0]

        if len(errored) == 0:
            print(
                "Successfully assembled {tgt}."
                .format(tgt=os.path.basename(self.target)), BR + GREEN)
            return True

        else:
            print("Found {i} errors:".format(i=len(errored)), BR + RED, BOLD)

            print("{div}\n{errors}\n{div}\n\n".format(
                div=self.__div,
                errors=('\n' + self.__div + '\n').join(
                    str(i) for i in errored)))


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
