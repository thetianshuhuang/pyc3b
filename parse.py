
import re


class Instruction:

    OPCODES = {
        "ADD": [0x1000, 'DR', 'SR1', 'op.spec'],
        "AND": [0x5000, 'DR', 'SR1', 'op.spec'],
        "BR": None,
        "BRN": None,
        "BRZ": None,
        "BRP": None,
        "BRNZ": None,
        "BRNP": None,
        "BRZP": None,
        "BRNZP": None,
        "JMP": None,
        "JSR": None,
        "JSRR": None,
        "LDB": None,
        "LDW": None,
        "LEA": None,
        "NOT": None,
        "RET": None,
        "RTI": None,
        "LSHF": None,
        "RSHFL": None,
        "RSHFA": None,
        "STB": None,
        "STW": None,
        "TRAP": None,
        "XOR": None,
        "HALT": None,
        "NOP": None,
        ".FILL": None,
        ".ORIG": None,
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
