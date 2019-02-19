

class AsmException(Exception):
    pass


class InvalidRegisterException(AsmException):
    pass


# Address
class AddressException(AsmException):
    pass


class InstructionBeforeOrigException(AddressException):
    pass


# Labels
class LabelException(AsmException):
    pass


class CannotStartWithXException(LabelException):
    "Labels cannot start with 'x'"
    pass


class ReservedNameException(LabelException):
    "Label cannot be IN, OUT, GETC, or PUTS"
    pass


class CharSetException(LabelException):
    "Label can only contain characters A-Z, 0-9"
    pass


class UndefinedLabelException(LabelException):
    pass


class RedefinedLabelException(LabelException):
    pass


class OffsetTooLargeException(LabelException):
    pass


class OffsetTooSmallException(LabelException):
    pass


# Constants
class InvalidConstantException(AsmException):
    pass


class InvalidDecException(InvalidConstantException):
    pass


class InvalidHexException(InvalidConstantException):
    pass


class ConstTooSmallException(InvalidConstantException):
    pass


class ConstTooLargeException(InvalidConstantException):
    pass
