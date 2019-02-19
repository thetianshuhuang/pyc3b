
from exceptions import *


class ParseMixins:

    def __reg(self, val):
        """Get register number

        Parameters
        ----------
        val : str
            Register number; should be R0-R7

        Returns
        -------
        int
            Integer 0-7

        Raises
        ------
        InvalidRegisterException
            Register is not R0-R7
        """
        assert val != '', InsufficientOperandsException()
        assert val[0] == 'R', InvalidRegisterException(val)
        try:
            x = int(val[1:])
            assert (0 <= x and x <= 7)
        except Exception:
            raise InvalidRegisterException(val)

        return x

    def __label(self, val, width=9):
        """Get label offset

        Parameters
        ----------
        val : str
            Input string
        width : int
            Bit-width of output offset

        Returns
        -------
        int
            PC offset of target label

        Raises
        ------
        UndefinedLabelException
            Label not found
        OffsetTooSmallException
            Instruction too far before PC to fit
        OffsetTooLargeException
            Instruction too far after PC to fit
        """
        assert val != '', InsufficientOperandsException()
        assert val in self.table, UndefinedLabelException(val)

        off = (self.table[val] - self.address - 2) // 2

        assert off < 2**(width - 1), OffsetTooSmallException(off, width)
        assert off >= -1 * 2**(width - 1), OffsetTooLargeException(off, width)

        return off

    def __imm(self, val, width=16, signed=None):
        """Get immediate value

        Parameters
        ----------
        val : str
            Constant operand
        width : int
            Width of constant operand
        signed : bool or None
            True: signed value; False: unsigned value; None: don't care

        Returns
        -------
        int
            Constant Value

        Raises
        ------
        InvalidDecException
            Decimal constant with invalid character[s]
        InvalidHexException
            Hex constant with invalid character[s]
        InvalidConstantException
            Neither decimal nor hex constant
        OffsetTooSmallException
            Offset smaller than integer min value
        OffsetTooLargeException
            Offset larger than integer min value
        """

        assert val != '', InsufficientOperandsException()

        # Parse value
        if val[0] == '#':
            try:
                val = int(val[1:])
            except ValueError:
                raise InvalidDecException(val)
        elif val[0] == 'X':
            try:
                val = int(val[1:], 16)
            except ValueError:
                raise InvalidHexException(val)
        else:
            raise InvalidConstantException(val)

        # Check bounds
        if signed is None:
            assert -1 * 2**(width - 1) <= val, OffsetTooSmallException(
                val, width, signed)
            assert val < 2**width, OffsetTooLargeException(
                val, width, signed)
        elif signed:
            assert -1 * 2**(width - 1) <= val, OffsetTooSmallException(
                val, width, signed)
            assert val < 2**(width - 1) - 1, OffsetTooLargeException(
                val, width, signed)
        else:
            assert 0 <= val, OffsetTooSmallException(
                val, width, signed)
            assert val < 2**width - 1, OffsetTooLargeException(
                val, width, signed)

        return val

    def DR(self, x):
        return self.__reg(x) << 9

    def SR1(self, x):
        return self.__reg(x) << 6

    def op_spec(self, x):
        try:
            return self.__reg(x)
        except (InvalidRegisterException, AssertionError):
            return 0x0020 | (self.__imm(x, width=5) & 0x001F)

    def PCoffset9(self, x):
        return self.__label(x, width=9) & 0x01FF

    def PCoffset11(self, x):
        return self.__label(x, width=11) & 0x07FF

    def offset6(self, x):
        return self.__imm(x, width=6, signed=True) & 0x003F

    def amount4(self, x):
        return self.__imm(x, width=4, signed=False) & 0x000F

    def trapvec8(self, x):
        return self.__imm(x, width=8, signed=False) & 0x00FF

    def fill(self, x):
        return self.__imm(x, width=16, signed=None)
