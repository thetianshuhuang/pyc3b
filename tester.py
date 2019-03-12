"""
     _    ___ _____      _____       _
    | |  / __|__ / |__  |_   _|__ __| |_ ___ _ _
    | |_| (__ |_ \ '_ \   | |/ -_|_-<  _/ -_) '_|
    |____\___|___/_.__/   |_|\___/__/\__\___|_|
    UT Austin EE460N LC3b Clock-Level Simulator Test Engine
    Tianshu Huang, Spring 2019
"""

import sys
import print as p
from src import TestCase

_SRC_PATH = "evil/evil_{}.asm"
_EXEC_TARGET = "a.out"
_UCODE_FILE = "ucode3"
_TEST_CASES = ['alu', 'jmp', 'memory', 'cc']
_OBJ_TMP_FILE = "__tmp__.obj"


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

    for evil in _TEST_CASES:
        if p.argparse.is_flag(evil):
            test(evil)
            exit(0)

    for evil in _TEST_CASES:
        test(evil)
