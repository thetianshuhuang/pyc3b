
import re
from print import *

from exceptions import *
from opcodes import OPCODES_FMT
from parse import ParseMixins


class Instruction(ParseMixins):

    ILLEGAL_LABELS = {
        r'$X(.*)': CannotStartWithXException,
        r'(IN)|(OUT)|(GETC)|(PUTS)': ReservedNameException,
        r'[^A-Z0-9]': CharSetException,
    }

    def __init__(self, line, table, maxwidth):

        self.table = table
        self.maxwidth = maxwidth

        self.raw = line.strip('\n')

        args = re.sub(
            r'([,\s+]+)', ' ',
            re.sub(r'(([\s,]*);(.*))|\n', '', line.upper())).split(" ")

        self.address = None
        self.assembled = None
        self.err = []
        self.label = args[0] if len(args) > 0 else None
        self.opcode = args[1] if len(args) > 1 else None
        self.args = args[2:]

    def assemble(self):

        if self.address is not None or self.opcode == '.ORIG':
            try:
                types = OPCODES_FMT[self.opcode]
                self.assembled = types[0]
                for t, arg in zip(types[1:], self.args):
                    self.assembled |= getattr(self, t)(arg)
            except Exception as e:
                self.err.append(e)

    def __update_table(self, addr):

        # Check for illegal labels
        for regex, explanation in self.ILLEGAL_LABELS.items():
            if re.search(regex, self.label):
                self.err.append(explanation(self.label))

        if self.label in self.table:
            self.err.append(RedefinedLabelException(self.label))
        else:
            self.table.update({self.label: addr})

    def assign(self, addr):
        if self.label != '':
            try:
                self.__update_table(addr)
            except Exception as e:
                self.err.append(e)

        if self.opcode == '.END':
            return -1
        elif self.opcode not in OPCODES_FMT or addr == -1:
            return addr
        else:
            if self.opcode == '.ORIG':
                return int(self.args[0][1:], 16)
            elif addr is None:
                self.err.append(InstructionBeforeOrigException())
                return addr
            else:
                self.address = addr
                return addr + 2

    def __hex_or_none(self, val):
        if val is not None:
            return "0x{:04X}".format(val)
        else:
            return " " * 6

    def __str__(self):

        self.err = [
            e.args[0] if isinstance(e, AssertionError) else e
            for e in self.err]

        # Errors
        if len(self.err) > 0:
            text = render(self.raw, BR + RED, BOLD)
            asm = render("0x????", BR + RED, BOLD)
        # Pseudo-ops
        elif self.opcode in [".END", ".ORIG", ".FILL"]:
            text = render(self.raw, BR + CYAN)
            asm = self.__hex_or_none(self.assembled)
        # Comment or label-only line
        elif (
                self.address is None and
                self.assembled is None and
                self.label == ''):
            if ';' in self.raw:
                text = render(self.raw, BR + BLUE)
            else:
                text = render(self.raw, BR + BLACK)
            asm = "      "
        # No errors
        else:
            text = self.raw
            asm = self.__hex_or_none(self.assembled)

        return "| {addr} | {out} | {raw} | {err}".format(
            raw=text + ' ' * (self.maxwidth - len(self.raw)),
            addr=self.__hex_or_none(self.address),
            err=self.err,
            out=asm)


def parse(file, t):

    f = open(file)
    lines = f.readlines()
    f.close()

    maxwidth = max(len(i) for i in lines)
    lines = [Instruction(i, t, maxwidth) for i in lines]

    return lines, maxwidth


if __name__ == "__main__":
    t = {}

    tgt = "../lc3b-ilevel/evil_cc.asm"
    # tgt = "test.asm"
    x, maxwidth = parse(tgt, t)

    out = open("out.obj", "w")

    addr = None
    for i in x:
        addr = i.assign(addr)

    print("Symbol Table:")
    table.table(
        [["Symbol", "Address"]] +
        [[key, "0x{:04X}".format(value)] for key, value in t.items()])

    print("""
+--------+--------+-{d}-+
|  Addr  |  Code  |  Source {p} | Errors
+--------+--------+-{d}-+""".format(d='-' * maxwidth, p=' ' * (maxwidth - 8)))
    for i in x:
        i.assemble()
        print(str(i))
        if i.assembled is not None:
            out.write("0x{:04X}\n".format(i.assembled))
    print("+--------+--------+-{d}-+".format(d='-' * maxwidth))
