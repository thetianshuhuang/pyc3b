
import re
from print import *

from opcodes import OPCODES_FMT
from parse import ParseMixins
from exceptions import *


class Instruction(ParseMixins):

    ILLEGAL_LABELS = {
        r'$X(.*)': CannotStartWithXException,
        r'(IN)|(OUT)|(GETC)|(PUTS)': ReservedNameException,
        r'[^A-Z0-9]': CharSetException,
    }

    def __init__(self, line, table, maxwidth, idx):

        self.table = table
        self.maxwidth = maxwidth
        self.linenum = idx

        self.raw = line.strip('\n')

        args = re.sub(
            r'([,\s+]+)', ' ',
            re.sub(r'(([\s,]*);(.*))|\n', '', line.upper())).split(" ")

        self.address = None
        self.assembled = None
        self.err = []
        self.label = args[0] if len(args) > 0 else None
        self.opcode = args[1] if len(args) > 1 else None
        self.args = args[2:] + ['', '', '']

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

        if addr is not None and addr > 0xFFFF:
            self.err.append(AddressOutOfBoundsException(addr))
        elif self.opcode == '.END':
            return -1
        elif self.opcode is None or addr == -1:
            return addr
        elif self.opcode not in OPCODES_FMT:
            self.err.append(InvalidOpcodeException(self.opcode))
            return addr
        else:
            if self.opcode == '.ORIG':
                try:
                    assert self.args[0][0] == 'X'
                    start = int(self.args[0][1:], 16)
                except Exception:
                    start = 0x3000
                    self.err.append(InvalidHexException(self.args[0]))
                if start % 2 != 0:
                    self.err.append(WordAlignmentException(self.args[0]))
                return start
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

        line = render(str(self.linenum), BR + BLACK)

        return "| {line} | {addr} | {out} | {raw} | {err}".format(
            line=line + ' ' * (4 - len(str(self.linenum))),
            raw=text + ' ' * (self.maxwidth - len(self.raw)),
            addr=self.__hex_or_none(self.address),
            err=" ".join([e.desc for e in self.err]),
            out=asm)
