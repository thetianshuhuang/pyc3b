"""Rdump Parse Class

Attributes
----------
_CSV_FMT : str
    Format string to use for CSV outputs of rdump states
_STDOUT_FMT : str
    Format string to use for normal (stdout) / readable outputs of rdump states
"""

import print as p


_CSV_FMT = "{},0x{:04X},0x{:04X},{},0x{:04X},0x{:04X},0x{:04X},{},{},{},{}"
_STDOUT_FMT = (
    '[{:03}]  pc: 0x{:04X}  ir: 0x{:04X}  st: {:02}  bus: 0x{:04X}  '
    'mdr: 0x{:04X}  mar: 0x{:04X}  nzp: {}  reg: {}')


def as_hex(x):
    """Helper function to convert label:value to int

    Parameters
    ----------
    x : str
        Input string - "label : 0xvalue\n"

    Returns
    -------
    int
        x(as hex) -> int
    """

    return int(x.split(':')[1][3:], 16)


class Rdump:
    """Rdump result parse, storage, and format class

    Parameters
    ----------
    x : str or dict
        Source values; either a dictionary of value, or the string output of
        the rdump commmand in the simulator
    """

    def __init__(self, x, prev):

        self.prev = prev

        if type(x) == str:
            self.__init_str(x)
        elif type(x) == dict:
            self.__init_dict(**x)

    def __init_str(self, s):
        """Initialize from string"""

        block = s.split('\n')
        comments = []

        for b in block:
            if b[:1] == '#':
                comments.append(b)
                block.remove(b)

        self.__init_dict(
            cycle=int(block[0].split(':')[1]),
            pc=as_hex(block[1]),
            ir=as_hex(block[2]),
            state=as_hex(block[3]),
            bus=as_hex(block[5]),
            mdr=as_hex(block[6]),
            mar=as_hex(block[7]),
            cc=[x[-1] for x in(block[8].split(':')[1]).split('  ')],
            registers=[as_hex(block[10 + i]) for i in range(8)],
            comments=comments)

    def __init_dict(
            self, cycle=0, pc=0, ir=0, state=0, bus=0,
            mdr=0, mar=0, cc=0, registers=0, comments=[]):
        """Initialize from dictionary (unpack before passing)"""

        self.cycle = cycle
        self.pc = pc
        self.ir = ir
        self.state = state
        self.bus = bus
        self.mdr = mdr
        self.mar = mar
        self.cc = cc
        self.registers = registers
        self.comments = comments

    def __eq__(self, other):
        """__eq__ overloading to facilitate comparisons"""

        return (
            self.pc == other.pc and self.ir == other.ir and
            self.state == other.state and self.bus == other.bus and
            self.mdr == other.mdr and self.mar == other.mar and
            self.cc == other.cc and self.registers == other.registers)

    def __str__(self):
        return _STDOUT_FMT.format(
            self.cycle, self.pc, self.ir, self.state,
            self.bus, self.mdr, self.mar,
            ''.join(self.cc),
            ' '.join("{:04X}".format(i) for i in self.registers))

    def str_color(self, nocomment=False):
        """Color output based on difference to previous cycle"""

        if self.prev is None:
            return self.__str__()

        prev = str(self.prev).split(' ')
        current = self.__str__().split(' ')

        base = ' '.join([
            p.render(i, p.BR + p.GREEN, p.BOLD)
            if i != j else i for i, j in zip(current, prev)])

        if nocomment:
            self.comments = []

        return '\n'.join(
            [base] +
            [p.render(c, p.BR + p.BLUE) for c in self.comments])

    def csv(self):
        """Get CSV output

        Returns
        -------
        str
            comma separated ouput, with integers (except for cycle_num, state)
            as hex.
        """
        return _CSV_FMT.format(
            self.cycle, self.pc, self.ir, self.state,
            self.bus, self.mdr, self.mar,
            self.cc[0], self.cc[1], self.cc[2],
            ','.join(["0x{:04X}".format(i) for i in self.registers]))
