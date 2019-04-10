r"""
     _    ___ _____      _____       _
    | |  / __|__ / |__  |_   _|__ __| |_ ___ _ _
    | |_| (__ |_ \ '_ \   | |/ -_|_-<  _/ -_) '_|
    |____\___|___/_.__/   |_|\___/__/\__\___|_|
    LC3b Clock-Level Simulator Test Engine
    Tianshu Huang, Spring 2019 -- EE 460N @ UT Austin (Yale Patt)

Usage : python tester.py [-flags]

Test cases should be in the folder 'evil/' in the project directory:
    evil/evil_alu.obj
    evil/evil_jmp.obj
    evil/evil_memory.obj
    evil/evil_cc.obj
The source simulator should be compiled to 'a.out'.
The source microcode file should be named 'ucode3'.

Flags
-----
--csv
    Use CSV output instead (echos to stdout -- must pipe)
--alu, --cc, --memory, --jmp, --all
    Only run the specified test case
"""

import sys
import print as p
from src import TestCase

# General
_EXEC_TARGET = "a.out"
_OBJ_TMP_FILE = "__tmp__.obj"

# Lab 3
_UCODE_FILE_3 = "ucode3"
_SRC_PATH = "evil/evil_{}.asm"
_TEST_CASES = ['alu', 'jmp', 'memory', 'cc']

# Lab 4
_UCODE_FILE_4 = "ucode4"
_DATA_FILE = "data.obj"
_TIMER_INT = "int.obj"
_PROT_EXC = "except_prot.obj"
_UNALIGNED_EXC = "except_unaligned.obj"
_UNKNOWN_EXC = "except_unknown.obj"
_VECTOR_TABLE = "vector_table.obj"


__HEADER = p.render(r"""
     _    ___ _____      _____       _
    | |  / __|__ / |__  |_   _|__ __| |_ ___ _ _
    | |_| (__ |_ \ '_ \   | |/ -_|_-<  _/ -_) '_|
    |____\___|___/_.__/   |_|\___/__/\__\___|_|
    LC3b Clock-Level Simulator Test Engine
    Tianshu Huang, Spring 2019 -- EE 460N @ UT Austin (Yale Patt)
""", p.BR + p.RED, p.BOLD)

__HINT = """
Usage : python tester.py [-flags]

Test cases should be in the folder 'evil/' in the project directory:
    evil/evil_alu.obj
    evil/evil_jmp.obj
    evil/evil_memory.obj
    evil/evil_cc.obj
The source simulator should be compiled to 'a.out'.
The source microcode file should be named 'ucode3'.

Flags
-----
-c / --csv
    Use CSV output instead (echos to stdout -- must pipe)
--alu, --cc, --memory, --jmp
    Only run the specified test case

"""


def test(e, lab=4):
    """Run test case"""

    if lab == 3:
        cmd = "./{} {} {}".format(
            _EXEC_TARGET, _UCODE_FILE_4, _OBJ_TMP_FILE)
    elif lab == 4:
        cmd = "./" + " ".join([
            _EXEC_TARGET, _UCODE_FILE_4, _OBJ_TMP_FILE,
            _DATA_FILE,
            _VECTOR_TABLE,
            _TIMER_INT,
            _PROT_EXC,
            _UNALIGNED_EXC,
            _UNKNOWN_EXC])

    t = TestCase(
        name=e,
        tgt=_SRC_PATH.format(evil),
        cmd=cmd,
        tmpfile=_OBJ_TMP_FILE)

    if p.argparse.is_flag('csv'):
        t.csv()
    else:
        t.print()


if __name__ == '__main__':

    # Don't print header if CSV output is selected
    if not p.argparse.is_flag('csv'):
        p.print(__HEADER)

    if p.argparse.is_flag('3'):
        lab = 3
    elif p.argparse.is_flag('4'):
        lab = 4
    else:
        lab = 3

    # Run all tests
    if p.argparse.is_flag('all'):
        for evil in _TEST_CASES:
            test(evil, lab=lab)
        exit(0)

    # Run single test
    for evil in _TEST_CASES:
        if p.argparse.is_flag(evil):
            test(evil, lab=lab)
            exit(0)

    # not exited yet -> no test specified
    p.print(__HINT)
