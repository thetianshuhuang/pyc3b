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

_RDUMP_HDR = (
    "Current register/bus values :\n"
    "-------------------------------------\n")


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
            cmd="./a.out ucode3 __tmp__.obj", tmpfile="__tmp__.obj"):

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

    def print(self):
        """Print test case output to stdout"""

        print(_STDOUT_HEADER.format(self.name, self.cmd))

        line_idx = 0
        for i in self.result:
            if i.state in [18, 19]:
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
            print(i.str_color())

    def csv(self):
        """Print test case output to stdout, formatted as csv"""

        print(_CSV_HEADER.format(self.name))
        for i in self.result:
            print(i.csv())
