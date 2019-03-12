r"""
     _    ___ _____      _____       _
    | |  / __|__ / |__  |_   _|__ __| |_ ___ _ _
    | |_| (__ |_ \ '_ \   | |/ -_|_-<  _/ -_) '_|
    |____\___|___/_.__/   |_|\___/__/\__\___|_|
    UT Austin EE460N LC3b Clock-Level Simulator Test Engine
    Tianshu Huang, Spring 2019

Usage : python tester.py [-flags]

Flags
-----
-c / --csv
    Use CSV output instead (echos to stdout -- must pipe)
--alu, --cc, --memory, --jmp, --all
    Only run the specified test case
"""

import sys
import print as p
from src import TestCase

_SRC_PATH = "evil/evil_{}.asm"
_EXEC_TARGET = "a.out"
_UCODE_FILE = "ucode3"
_TEST_CASES = ['alu', 'jmp', 'memory', 'cc']
_OBJ_TMP_FILE = "__tmp__.obj"

__HEADER = p.render(r"""
     _    ___ _____      _____       _
    | |  / __|__ / |__  |_   _|__ __| |_ ___ _ _
    | |_| (__ |_ \ '_ \   | |/ -_|_-<  _/ -_) '_|
    |____\___|___/_.__/   |_|\___/__/\__\___|_|
    UT Austin EE460N LC3b Clock-Level Simulator Test Engine
    Tianshu Huang, Spring 2019
""", p.BR + p.RED, p.BOLD)

__HINT = """
Usage : python tester.py [-flags]

Flags
-----
-c / --csv
    Use CSV output instead (echos to stdout -- must pipe)
--alu, --cc, --memory, --jmp
    Only run the specified test case

"""


def test(e):
    """Run test case"""

    t = TestCase(
        name=e,
        tgt=_SRC_PATH.format(evil),
        cmd="./{} {} {}".format(_EXEC_TARGET, _UCODE_FILE, _OBJ_TMP_FILE),
        tmpfile=_OBJ_TMP_FILE)

    if p.argparse.is_flag('c') or p.argparse.is_flag('csv'):
        t.csv()
    else:
        t.print()


if __name__ == '__main__':

    # Don't print header if CSV output is selected
    if not (p.argparse.is_flag('csv') or p.argparse.is_flag('c')):
        p.print(__HEADER)

    # Run all tests
    if p.argparse.is_flag('all'):
        for evil in _TEST_CASES:
            test(evil)
        exit(0)

    # Run single test
    for evil in _TEST_CASES:
        if p.argparse.is_flag(evil):
            test(evil)
            exit(0)

    # not exited yet -> no test specified
    p.print(__HINT)
