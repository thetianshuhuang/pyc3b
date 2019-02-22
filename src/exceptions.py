"""Assembler Exceptions

Attributes
----------
AsmException
    Generic exception base
InvalidRegisterException
    Register name not R0-R7
AddressException
    Address exception base
InstructionBeforeOrigException
    Instruction occurs before .ORIG
WordAlignmentException
    .ORIG not word aligned
LabelException
    Base exception for labels
CannotStartWithXException
    Labels must not start with 'X'
ReservedNameException
    Labels cannot be IN, OUT, GETC, or PUTS
CharSetException
    Labels can only use the characters A-Z, 0-9
UndefinedLabelException
    Referenced label is not defined
RedefinedLabelException
    Label is already in use
OffsetToolLargeException
    Offset required for this label is too large
OffsetTooSmallException
    Offset required for this label is too small
InvalidConstantException
    Base exception for constants
InvalidDecException
    Is not a valid decimal constant
InvalidHexException
    Is not a valid hex constant
ConstTooSmallException
    Constant is too small for this operand
ConstTooLargeException
    Constant is too large for this operand
"""


# -- Base ---------------------------------------------------------------------

class AsmException(Exception):
    desc = "Generic exception"


# -- Registers ----------------------------------------------------------------

class InvalidRegisterException(AsmException):
    desc = "Register must be R0-R7"


# -- Opcode -------------------------------------------------------------------

class InvalidOpcodeException(AsmException):
    desc = "Invalid opcode"


class InsufficientOperandsException(AsmException):
    desc = "Not enough operands for this instruction"


# -- Address ------------------------------------------------------------------

class AddressException(AsmException):
    desc = "Generic address exception"


class AddressOutOfBoundsException(AddressException):
    desc = "Address exceeds memory size (must be <0xFFFF)"


class InstructionBeforeOrigException(AddressException):
    desc = "Instructions cannot occur before .ORIG"


class WordAlignmentException(AddressException):
    desc = ".ORIG is not word aligned"


# -- Labels -------------------------------------------------------------------

class LabelException(AsmException):
    desc = "Generic label exception"


class CannotStartWithXException(LabelException):
    desc = "Labels cannot start with 'x'"


class ReservedNameException(LabelException):
    desc = "Labels cannot be IN, OUT, GETC, or PUTS"


class CharSetException(LabelException):
    desc = "Labels can only contain characters A-Z, 0-9"


class UndefinedLabelException(LabelException):
    desc = "Referenced label is not defined"


class RedefinedLabelException(LabelException):
    desc = "Label is already defined"


class OffsetTooLargeException(LabelException):
    desc = "Offset required for this label is too large for this operand"


class OffsetTooSmallException(LabelException):
    desc = "Offset required for this label is too small for this operand"


# Constants
class InvalidConstantException(AsmException):
    desc = "Constant is neither decimal (#0000) or hex (x0000)"


class InvalidDecException(InvalidConstantException):
    desc = "Constant is not a valid decimal number"


class InvalidHexException(InvalidConstantException):
    desc = "Constant is not a valid hex number"


class ConstTooSmallException(InvalidConstantException):
    desc = "Constant is too small for this operand"


class ConstTooLargeException(InvalidConstantException):
    desc = "Constant is too large for this operand"
