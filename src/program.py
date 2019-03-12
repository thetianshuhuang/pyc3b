"""LC3b Assembly Program Class

Usage
-----
p = Program("target.obj").assemble()
"""


import os
from print import *

from .exceptions import *
from .instruction import Instruction


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
            "+----------------------------------{b}-+\n"
            "| Assembled Program                {p} |\n"
            "{div}\n"
            "| Line |  Addr  |  Code  |  Source {p} |{e}\n"
            "{div}\n"
            "{code}\n"
            "{div}\n\n"
            .format(
                p=' ' * (self.maxwidth - 8),
                b='-' * (self.maxwidth - 8),
                div=self.__div,
                code="\n".join(str(i) for i in self.instructions),
                e=' Errors' if self.is_errored() else ''))

    def save_output(self, file, silent=False):
        """Save output to file

        Parameters
        ----------
        file : str
            Output file
        silent : bool
            Supress status message?
        """
        with open(file, "w") as out:
            for i in self.instructions:
                if i.assembled is not None:
                    out.write("0x{:04X}\n".format(i.assembled))

        if not silent:
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
