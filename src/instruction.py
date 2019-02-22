"""Instruction parse and assembly

Usage
-----
Run first pass by calling Instruction.assign(addr) for a address counter addr.
Run second pass by calling Instruction.assemble()
Fetch output with Instruction.assembled
"""

import re
from print import *

from .opcodes import OPCODES_FMT
from .parse import ParseMixins
from .exceptions import *

_ILLEGAL_LABELS = {
    r'$X(.*)': CannotStartWithXException,
    r'(IN)|(OUT)|(GETC)|(PUTS)': ReservedNameException,
    r'[^A-Z0-9]': CharSetException,
}


class Instruction(ParseMixins):
    """Instruction object

    Parameters
    ----------
    line : str
        Assembly code
    table : dict[str]->int
        Reference to symbol table
    maxwidth : int
        Text width
    idx : int
        Line number
    """

    def __init__(self, line, table={}, maxwidth=0, linenum=0):

        self.table = table
        self.maxwidth = maxwidth
        self.linenum = linenum

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

    def __try_or_log(self, f, *args, default=None, **kwargs):
        """Run a function;
        on Exception, log the exception and return default

        Parameters
        ----------
        f : function
            Function to run
        *args : list
            Args
        **kwargs : dict
            Kwargs
        default : arbitrary type
            Default return value
        """

        try:
            return f(*args, **kwargs)
        except Exception as e:
            self.err.append(e)
            return default

    def __build_ins(self):
        """Build a single instruction"""

        types = OPCODES_FMT[self.opcode]
        self.assembled = types[0]
        for t, arg in zip(types[1:], self.args):
            self.assembled |= getattr(self, t)(arg)

    def assemble(self):
        """Assemble the instruction; call this method on second pass"""

        if self.address is not None or self.opcode == '.ORIG':
            self.__try_or_log(self.__build_ins)

    def __update_table(self, addr):
        """Update symbol table

        Parameters
        ----------
        addr : int
            Current address
        """

        # Check for illegal labels
        for regex, explanation in _ILLEGAL_LABELS.items():
            if re.search(regex, self.label):
                self.err.append(explanation(self.label))

        if self.label in self.table:
            self.err.append(RedefinedLabelException(self.label))
        else:
            self.table.update({self.label: addr})

    def __handle_orig(self):
        """Handle .ORIG instruction

        Returns
        -------
        int
            Starting address
        """
        assert self.args[0][0] == 'X', InvalidHexException(self.args[0])
        start = int(self.args[0][1:], 16)
        assert start % 2 == 0, WordAlignmentException(self.args[0])
        return start

    def assign(self, addr):
        """Assign instruction address

        Parameters
        ----------
        addr : int
            Current memory address

        Returns
        -------
        int
            Updated memory address (incremented by 2 if instruction is valid)
        """

        # Update symbol table
        if self.label != '':
            self.__try_or_log(self.__update_table, addr)

        if addr is not None and addr > 0xFFFF:
            self.err.append(AddressOutOfBoundsException(addr))
        elif self.opcode == '.END':
            return -1
        elif self.opcode is None or self.opcode == '' or addr == -1:
            return addr
        elif self.opcode not in OPCODES_FMT:
            self.err.append(InvalidOpcodeException(self.opcode))
            return addr
        else:
            if self.opcode == '.ORIG':
                return self.__try_or_log(self.__handle_orig, default=0x0000)
            elif addr is None:
                self.err.append(InstructionBeforeOrigException())
                return addr
            else:
                self.address = addr
                return addr + 2

    def __hex_or_none(self, val):
        """Format hex value or None

        Parameters
        ----------
        val : int or None
            Value to format

        Returns
        -------
        str
            0x???? or "      " (if val is None)
        """
        if val is not None:
            return "0x{:04X}".format(val)
        else:
            return " " * 6

    def __str__(self):
        """Get string representation

        Returns
        -------
        str
            | line number | address | machine code | assembly code | errors
        """

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

        line = render(str(self.linenum), BR + BLUE)

        return "| {line} | {addr} | {out} | {raw} | {err}".format(
            line=line + ' ' * (4 - len(str(self.linenum))),
            raw=text + ' ' * (self.maxwidth - len(self.raw)),
            addr=self.__hex_or_none(self.address),
            err=" ".join([e.desc for e in self.err]),
            out=asm)
