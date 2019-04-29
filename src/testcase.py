"""General LC3b simulator Test Case class

Parameters
----------
"""

import subprocess
from .program import Program
from .rdump import Rdump
import print as p


_STDOUT_HEADER = """

       [evil_{}]
       {}
"""
_STDOUT_ASM_HEADER = (
    "-{ln:03}-  pc: 0x{pc:04X}  ir: 0x{ir:04X}  src: \"{raw}\"")
_CSV_HEADER = """evil_{}
cycle,pc,ir,state,bus,mdr,mar,n,z,p,r0,r1,r2,r3,r4,r5,r6,r7"""
_HIDDEN_HEADER = """
    [output hidden : PC in {}]

"""
_RDUMP_HDR = (
    "Current register/bus values :\n"
    "-------------------------------------\n")
_ISRS = {
    0x1200: "TIMER ISR",
    0x1400: "PAGE FAULT",
    0x1600: "PROTECTION EXCEPTION",
    0x1A00: "UNALIGNED ACCESS",
    0x1C00: "UNKNOWN OPCODE"
}
_ISR_HEADER = """
    <<< {} >>>

"""


class TestCase:
    """Test Case class

    Parameters
    ----------
    name : str
        Test case name
    tgt : str
        Target asm file
    cmd : str
        Command to run simulator
    tmpfile : str
        Temporary file to compile to (should match target in cmd)
    """

    def __get_ins(self, addr):
        """Get instruction at an address

        Parameters
        ----------
        addr : int
            Target memory address

        Returns
        -------
        Instruction
            Found instruction class. If the target address does not exist in
            the compiled program, returns the last line.
        """

        for i in self.src.instructions:
            if i.address == addr:
                return i
        return self.src.instructions[-1]

    def __init__(
            self, name="alu", tgt="evil/alu_alu.asm",
            cmd="./a.out ucode3 __tmp__.obj", tmpfile="__tmp__.obj",
            hide_range=[0, 0], ins_only=False, nocomment=True):

        # Settings
        self.hide_range = hide_range
        self.ins_only = ins_only
        self.nocomment = nocomment

        # Assemble target
        self.name = name
        self.src = Program(tgt).assemble()
        self.src.save_output(tmpfile, silent=True)

        # Run target
        self.cmd = cmd
        output = subprocess.check_output(
            cmd, shell=True).decode('utf-8').split(_RDUMP_HDR)[1:]

        # Parse target
        self.result = []
        for s in output:
            if len(self.result) == 0:
                self.result.append(Rdump(s, None))
            else:
                self.result.append(Rdump(s, self.result[-1]))

    def __print_line(self, i):
        if i.state in [18, 19]:

            if i.pc in _ISRS:
                p.print(_ISR_HEADER.format(_ISRS[i.pc]), p.BOLD, p.RED)

            try:
                ins = self.__get_ins(i.pc)
                p.print(
                    _STDOUT_ASM_HEADER.format(
                        ln=ins.linenum,
                        pc=ins.address,
                        ir=ins.assembled,
                        op=ins.opcode,
                        raw=ins.raw),
                    p.BOLD, p.BR + p.BLUE)
            except Exception as e:
                p.print(
                    "Could not find instruction. Is this instruction in "
                    "the target assembly file?",
                    p.BOLD, p.BR + p.BLACK)

        if i.state in [18, 19] or not self.ins_only:
            print(i.str_color(nocomment=self.nocomment))

    def print(self):
        """Print test case output to stdout"""

        print(_STDOUT_HEADER.format(self.name, self.cmd))

        in_hiding = False
        for i in self.result:
            if self.hide_range[0] < i.pc and i.pc < self.hide_range[1]:
                if not in_hiding:
                    in_hiding = True
                    p.print(_HIDDEN_HEADER.format(self.hide_range))
            else:
                self.__print_line(i)

    def csv(self):
        """Print test case output to stdout, formatted as csv"""

        print(_CSV_HEADER.format(self.name))
        for i in self.result:
            print(i.csv())
