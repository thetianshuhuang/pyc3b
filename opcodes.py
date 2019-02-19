
"""Instruction opcode-operand formats

Attributes
----------
OPCODES_FMT : dict[str]->[int, str, ...]
    The first entry of each list is the base opcode; each subsequent
    argument is fetched from ParseMixins, executed, and or'd to the
    base opcode
"""

OPCODES_FMT = {
    "ADD": [0x1000, 'DR', 'SR1', 'op_spec'],
    "AND": [0x5000, 'DR', 'SR1', 'op_spec'],
    "BR": [0x0E00, 'PCoffset9'],
    "BRN": [0x0800, 'PCoffset9'],
    "BRZ": [0x0400, 'PCoffset9'],
    "BRP": [0x0200, 'PCoffset9'],
    "BRNZ": [0x0C00, 'PCoffset9'],
    "BRNP": [0x0A00, 'PCoffset9'],
    "BRZP": [0x0600, 'PCoffset9'],
    "BRNZP": [0x0E00, 'PCoffset9'],
    "JMP": [0xC000, 'SR1'],
    "JSR": [0x4800, 'PCoffset11'],
    "JSRR": [0x4000, 'SR1'],
    "LDB": [0x2000, 'DR', 'SR1', 'offset6'],
    "LDW": [0x6000, 'DR', 'SR1', 'offset6'],
    "LEA": [0xE000, 'DR', 'PCoffset9'],
    "NOT": [0x903F, 'DR', 'SR1'],
    "RET": [0xC1C0],
    "RTI": [0x8000],
    "LSHF": [0xD000, 'DR', 'SR1', 'amount4'],
    "RSHFL": [0xD010, 'DR', 'SR1', 'amount4'],
    "RSHFA": [0xD030, 'DR', 'SR1', 'amount4'],
    "STB": [0x3000, 'DR', 'SR1', 'offset6'],
    "STW": [0x7000, 'DR', 'SR1', 'offset6'],
    "TRAP": [0xF000, 'trapvec8'],
    "XOR": [0x9000, 'DR', 'SR1', 'op_spec'],
    "HALT": [0xF025],
    "NOP": [0x0000],
    ".FILL": [0x0000, 'fill'],
    ".ORIG": [0x0000, 'fill'],
}
