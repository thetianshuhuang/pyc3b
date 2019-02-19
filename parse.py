
import re
import collections

ifmt = collections.namedtuple('ifmt', ['argtype', 'width', 'signed'])


DR = ifmt(argtype='REG')
SR1 = ifmt(argtype='REG')
SR2 = ifmt(argtype='REG')
op_spec = ifmt(argtype='')
PCoffset9 = ifmt(argtype='LABEL', width=9, signed=True)
PCoffset11 = ifmt(argtype='LABEL', width=11, signed=True)
offset6 = ifmt(argtype='IMM', width=6, signed=True)
amount4 = ifmt(argtype='IMM', width=4, signed=False)
trapvec8 = ifmt(argtype='IMM', width=8, signed=True, force_hex=True)
fill = ifmt(argtype='IMM', width=16, signed=None)


class Instruction:

    OPCODES = {
        "ADD": [0x1000, DR, SR1, op_spec],
        "AND": [0x5000, DR, SR1, op_spec],
        "BR": [0x0E00, PCoffset9],
        "BRN": [0x0800, PCoffset9],
        "BRZ": [0x0400, PCoffset9],
        "BRP": [0x0200, PCoffset9],
        "BRNZ": [0x0C00, PCoffset9],
        "BRNP": [0x0A00, PCoffset9],
        "BRZP": [0x0600, PCoffset9],
        "BRNZP": [0x0E00, PCoffset9],
        "JMP": [0xC000, SR1],
        "JSR": [0x4800, PCoffset11],
        "JSRR": [0x4000, SR1],
        "LDB": [0x2000, DR, SR1, offset6],
        "LDW": [0x6000, DR, SR1, offset6],
        "LEA": [0xE000, SR1, PCoffset9],
        "NOT": [0x903F, DR, SR1],
        "RET": [0xC1C0],
        "RTI": [0x8000],
        "LSHF": [0xD000, DR, SR1, amount4],
        "RSHFL": [0xD010, DR, SR1, amount4],
        "RSHFA": [0xD030, DR, SR1, amount4],
        "STB": [0x3000, DR, SR1, offset6],
        "STW": [0x7000, DR, SR1, offset6],
        "TRAP": [0xF000, trapvec8],
        "XOR": [0x9000, DR, SR1, op_spec],
        "HALT": [0xF025],
        "NOP": [0x0000],
        ".FILL": [fill],
        ".ORIG": [fill],
    }

    ILLEGAL_LABELS = {
        r'$X(.*)': "Labels cannot start with 'x'",
        r'(IN)|(OUT)|(GETC)|(PUTS)': "Label cannot be IN, OUT, GETC, or PUTS",
        r'^[A-Z0-9]': "Label can only contain characters A-Z, 0-9",
    }

    def __init__(self, line):

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

        self.OPCODES[self.opcode]

    def assign(self, addr, table):
        if self.label is not None:
            for regex, explanation in self.ILLEGAL_LABELS.items():
                if re.match(regex, self.label):
                    self.err += explanation
            if self.label in table:
                self.err += 'Label already in use: ' + self.label
            table.update({self.label: addr})

        if self.opcode not in self.OPCODES:
            return addr
        else:
            if self.opcode == '.ORIG':
                return int(self.args[0][1:], 16)
            elif addr is None:
                self.err += 'Intruction before .ORIG'
                return addr
            else:
                self.address = addr
                return addr + 2

    def __hex_or_none(self, val):
        if val is not None:
            return "0x{:04x}".format(val)
        else:
            return " " * 6

    def __str__(self):

        return " {addr} {out} {raw} {err}".format(
            raw=self.raw + ' ' * (50 - len(self.raw)),
            addr=self.__hex_or_none(self.address),
            err="",
            out=self.__hex_or_none(self.assembled))


def parse(file):

    f = open(file)
    lines = f.readlines()
    f.close()

    lines = [Instruction(i) for i in lines]

    return lines


if __name__ == "__main__":
    x = parse("../lc3b-ilevel/evil_cc.asm")
    t = {}

    addr = None
    for i in x:
        addr = i.assign(addr, t)

    for i in x:
        print(str(i))
