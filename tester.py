import subprocess
import sys
import collections
import print as p
from src import Program


def as_hex(x):
    return int(x.split(':')[1][3:], 16)


class Rdump:

    def __init__(self, x, prev):

        self.prev = prev

        if type(x) == str:
            self.__init_str(x)
        elif type(x) == dict:
            self.__init_dict(**x)

    def __init_str(self, s):

        block = s.split('\n')
        self.__init_dict(
            cycle=int(block[2].split(':')[1]),
            pc=as_hex(block[3]),
            ir=as_hex(block[4]),
            state=as_hex(block[5]),
            bus=as_hex(block[7]),
            mdr=as_hex(block[8]),
            mar=as_hex(block[9]),
            cc=[x[-1] for x in(block[10].split(':')[1]).split('  ')],
            registers=[as_hex(block[12 + i]) for i in range(8)])

    def __init_dict(
            self, cycle=0, pc=0, ir=0, state=0, bus=0,
            mdr=0, mar=0, cc=0, registers=0):

        self.cycle = cycle
        self.pc = pc
        self.ir = ir
        self.state = state
        self.bus = bus
        self.mdr = mdr
        self.mar = mar
        self.cc = cc
        self.registers = registers

    def __eq__(self, other):
        return (
            self.pc == other.pc and self.ir == other.ir and
            self.state == other.state and self.bus == other.bus and
            self.mdr == other.mdr and self.mar == other.mar and
            self.cc == other.cc and self.registers == other.registers)

    def __str__(self):

        return (
            '[{:03}]  pc: 0x{:03X}  ir: 0x{:04X}  st: {:02}  '
            'bus: 0x{:04X}  mdr: 0x{:04X}  mar: 0x{:04X}  nzp: {}  '
            'reg: {}'
            ''.format(
                self.cycle, self.pc, self.ir, self.state,
                self.bus, self.mdr, self.mar,
                ''.join(self.cc),
                ' '.join("{:04X}".format(i) for i in self.registers)))

    def str_color(self):
        if self.prev is None:
            return self.__str__()

        prev = str(self.prev).split(' ')
        current = self.__str__().split(' ')

        return ' '.join([
            p.render(i, p.BR + p.GREEN, p.BOLD)
            if i != j else i for i, j in zip(current, prev)])


class Evil:

    def __get_ins(self, addr):

        for i in self.src.instructions:
            if i.address == addr:
                return i
        return self.src.instructions[-1]

    def __init__(self, tgt):

        self.src = Program(tgt).assemble()
        self.src.save_output("__tmp__.obj")

        output = subprocess.check_output(
            "./a.out ucode3 __tmp__.obj", shell=True
        ).decode('utf-8').split('\n\n\n')[1:]

        self.result = []
        for s in output:
            if len(self.result) == 0:
                self.result.append(Rdump(s, None))
            else:
                self.result.append(Rdump(s, self.result[-1]))

        line_idx = 0
        for i in self.result:
            if i.state == 18:
                ins = self.__get_ins(i.pc)
                p.print(
                    "-{ln:03}-  pc: 0x{pc:04X}  "
                    "ir: 0x{ir:04X}  src: \"{op} {args}\"".format(
                        ln=ins.linenum,
                        pc=ins.address,
                        ir=ins.assembled,
                        op=ins.opcode,
                        args=', '.join([i for i in ins.args if i != ''])),
                    p.BOLD, p.BR + p.BLUE)

            print(i.str_color())


def test(evil):

    Evil('evil/evil_' + evil + '.asm')


if __name__ == '__main__':
    test(sys.argv[1])
