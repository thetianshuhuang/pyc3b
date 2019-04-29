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
--csv (-c)
    Use CSV output instead (echos to stdout -- must pipe)
--alu, --cc, --memory, --jmp, --add, --all
    Only run the specified test case
-3, -4, -5:
    Specify target lab
--getcmd (-g)
    Get command to use with vanilla tool instead of running the tester
--ins (-i)
    Show instructions only (don't elaborate on clocks within each instruction)
--nc (-c)
    Hide comments
--noint (-n)
    Hide ISR (int.asm) (since it takes up ~25k cycles)
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
_SRC_PATH_4 = "evil4/{}"
_DATA_FILE_4 = "data.obj"
_TIMER_INT_4 = "int.obj"
_PROT_EXC_4 = "except_prot.obj"
_UNALIGNED_EXC_4 = "except_unaligned.obj"
_UNKNOWN_EXC_4 = "except_unknown.obj"
_VECTOR_TABLE_4 = "vector_table.obj"
_TEST_CASES_4 = ['add']

# lab 5
_UCODE_FILE_5 = "ucode5"
_SRC_PATH_5 = "evil5/{}"
_DATA_FILE_5 = "data.obj"
_TIMER_INT_5 = "int.obj"  # should trasverse PT, clear R bits
_PROT_EXC_5 = "except_prot.obj"
_UNALIGNED_EXC_5 = "except_unaligned.obj"
_UNKNOWN_EXC_5 = "except_unknown.obj"
_PF_EXC_5 = "except_page.obj"
_VECTOR_TABLE_5 = "vector_table.obj"
_PAGE_TABLE_5 = "page_table.obj"
_TEST_CASES_5 = ['add']


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
--csv (-c)
    Use CSV output instead (echos to stdout -- must pipe)
--alu, --cc, --memory, --jmp, --add, --all
    Only run the specified test case. NOTE: --add is only supported for labs
    4 and 5
-3, -4, -5:
    Specify target lab
--getcmd (-g)
    Get command to use with vanilla tool instead of running the tester
--ins (-i)
    Show instructions only (don't elaborate on clocks within each instruction)
--nc (-c)
    Hide comments
--noint (-n)
    Hide ISR (int.asm) (since it takes up ~25k cycles)

"""

__CMD_DISP = """
Command to use vanilla command-line tool:

{}
"""


def get_cmd_4():
    srcs = [_SRC_PATH_4.format(s) for s in [
        _DATA_FILE_4,
        _VECTOR_TABLE_4,
        _TIMER_INT_4,
        _PROT_EXC_4,
        _UNALIGNED_EXC_4,
        _UNKNOWN_EXC_4
    ]]

    cmd = "./" + " ".join(
        [_EXEC_TARGET, _UCODE_FILE_4, _OBJ_TMP_FILE] + srcs)

    return cmd


def get_cmd_5():
    srcs = [_SRC_PATH_5.format(s) for s in [
        _DATA_FILE_5,
        _VECTOR_TABLE_5,
        _TIMER_INT_5,
        _PROT_EXC_5,
        _UNALIGNED_EXC_5,
        _UNKNOWN_EXC_5,
        _PF_EXC_5,
    ]]

    cmd = "./" + " ".join(
        [
            _EXEC_TARGET,
            _UCODE_FILE_5,
            _SRC_PATH_5.format(_PAGE_TABLE_5),
            _OBJ_TMP_FILE
        ] + srcs)

    return cmd


def test(e, lab=4):
    """Run test case"""

    if lab == 3:
        cmd = "./{} {} {}".format(
            _EXEC_TARGET, _UCODE_FILE_4, _OBJ_TMP_FILE)
        tgt = _SRC_PATH.format(evil)

    elif lab == 4:
        cmd = get_cmd_4()

        if p.argparse.is_flag('add'):
            tgt = "evil4/add.asm"
        else:
            tgt = _SRC_PATH.format(evil)

    elif lab == 5:
        cmd = get_cmd_5()

        if p.argparse.is_flag('add'):
            tgt = "evil5/add.asm"
        else:
            tgt = _SRC_PATH.format(evil)

    if p.argparse.is_flag('getcmd') or p.argparse.is_flag('g'):
        print(__CMD_DISP.format(cmd))

    else:
        hide_range = (
            [0x1200, 0x1400] if
            (p.argparse.is_flag('noint') or p.argparse.is_flag('n'))
            else [0, 0])

        t = TestCase(
            name=e, tgt=tgt, cmd=cmd, tmpfile=_OBJ_TMP_FILE,
            hide_range=hide_range,
            ins_only=p.argparse.is_flag('ins') or p.argparse.is_flag('i'),
            nocomment=p.argparse.is_flag('nc') or p.argparse.is_flag('c'))

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
    elif p.argparse.is_flag('5'):
        lab = 5
    else:
        lab = 3

    # Run all tests
    if p.argparse.is_flag('all'):
        for evil in _TEST_CASES:
            test(evil, lab=lab)
        exit(0)

    # Run single test
    for evil in _TEST_CASES + _TEST_CASES_4:
        if p.argparse.is_flag(evil):
            test(evil, lab=lab)
            exit(0)

    # not exited yet -> no test specified
    p.print(__HINT)
