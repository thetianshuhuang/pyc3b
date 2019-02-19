
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

__HINT = """
Usage
-----
"""


class Program:

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
                i, self.symbol_table, self.maxwidth, idx)
            for idx, i in enumerate(lines)]

    def first_pass(self):
        addr = None

        for i in self.instructions:
            addr = i.assign(addr)

    def second_pass(self):
        for i in self.instructions:
            i.assemble()

    def print_symbols(self):
        print("Symbol Table:")
        table.table(
            [["Symbol", "Address"]] + [
                [key, "0x{:04X}".format(value)]
                for key, value in self.symbol_table.items()
            ])

    def print_program(self):
            print(
                "{div}\n| Line |  Addr  |  Code  |  Source {p} | Errors\n{div}"
                .format(
                    p=' ' * (self.maxwidth - 8), div=self.__div))
            for i in self.instructions:
                print(str(i))
            print(self.__div)

    def save_output(self, file):
        with open(file, "w") as out:
            for i in self.instructions:
                if i.assembled is not None:
                    out.write("0x{:04X}\n".format(i.assembled))

    def summary(self):

        errored = [i for i in self.instructions if len(i.err) > 0]

        if len(errored) == 0:
            print(
                "Successfully assembled {tgt}."
                .format(tgt=self.target), BR + GREEN)
            return True

        else:
            print("Found {i} errors:".format(i=len(errored)))
            print(self.__div)
            for i in errored:
                print(str(i))
                print(self.__div)
            return False


if __name__ == "__main__":

    import sys
    tgt = (sys.argv + [''])[1]
    flags = (sys.argv + ['', ''])[2]

    print(__HEADER)

    p = Program(tgt)

    out = open("out.obj", "w")

    p.first_pass()
    p.second_pass()

    if 't' in flags:
        p.print_symbols()
    if 'p' in flags:
        p.print_program()

    if p.summary():
        p.save_output('out.obj')
