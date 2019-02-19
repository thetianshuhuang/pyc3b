
import re


class Instruction:

    def __init__(self, line):

        self.raw = line.strip('\n')

        args = re.sub(
            r'([,\s+]+)', ' ',
            re.sub(r'(([\s,]*);(.*))|\n', '', line)).split(" ")

        self.address = None
        self.assembled = None
        self.err = ""
        self.label = args[0] if len(args) > 0 else None
        self.opcode = args[1] if len(args) > 1 else None
        self.args = args[2:]

    def __hex_or_none(self, val):
        if val is not None:
            return "0x{:04x}".format(val)
        else:
            return " " * 6

    def __str__(self):

        return " {addr} {out} {raw} {err}".format(
            raw=self.raw + ' ' * (50 - len(self.raw)),
            addr=self.__hex_or_none(self.address),
            err=self.err,
            out=self.__hex_or_none(self.assembled))


def parse(file):

    f = open(file)
    lines = f.readlines()
    f.close()

    lines = [Instruction(i) for i in lines]

    return lines


if __name__ == "__main__":
    for i in parse("../lc3b-ilevel/evil_cc.asm"):
        print(str(i))
