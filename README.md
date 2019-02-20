# pyc3b

Python PC3b Assembler

![](https://github.com/thetianshuhuang/pyc3b/blob/master/wide.png)

## Dependencies
- Python 3
- [print](https://github.com/thetianshuhuang/print)

## Usage
```shell
$ python assemble.py source [output] [-flags]
```

### Arguments
- ```source```: Source LC3b assembly file
- ```output```: Optional output file; defaults to the same name as source, except with a ```.obj``` extension

### Flags
- ```-p```: Print out assembled files
- ```-t```: Print out symbol table

## Sample Session
```
$ python assemble.py test.asm -pt

     _____   _____ _____
    | _ \ \ / / __|__ / |__
    |  _/\ V / (__ |_ \ '_ \
    |_|   |_| \___|___/_.__/
    Python LC3b Assembler

Symbol Table
+------+-------+
|Symbol|Address|
+------+-------+
|LABEL |0x0000 |
+------+-------+
|LA    |0x0008 |
+------+-------+
|GETCH |0x0010 |
+------+-------+
|A     |0x0024 |
+------+-------+

Assembled Program
+------+--------+--------+---------------------------------------+
| Line |  Addr  |  Code  |  Source                               | Errors
+------+--------+--------+---------------------------------------+
| 0    |        |        | ; check ALU instructions              |
| 1    |        |        |                                       |
| 2    |        | 0x???? |     ADD R0, R0, R2                    | Instructions cannot occur before .ORIG
| 3    |        |        |                                       |
| 4    |        | 0x???? |     .ORIG x3001                       | .ORIG is not word aligned
| 5    |        |        |                                       |
| 6    |        |        | Label                                 |
| 7    | 0x0000 | 0x5020 |     AND R0, R0, #0                    |
| 8    | 0x0002 | 0x1025 |     ADD R0, R0, #5      ; R0: 0x0005  |
| 9    | 0x0004 | 0x1236 |     ADD R1, R0, #-10    ; R1: 0xFFF6  |
| 10   | 0x0006 | 0x54A0 |     AND R2, R2, #0                    |
| 11   | 0x0008 | 0x14BF | LA  ADD R2, R2, #-1     ; R2: 0xFFFF  |
| 12   | 0x000A | 0x96BF |     NOT R3, R2          ; R3: 0x0000  |
| 13   |        |        |                                       |
| 14   | 0x000C | 0x???? |     LDB R0, #2                        | Register must be R0-R7
| 15   | 0x000E | 0x???? |     LDW R12, R0, #0                   | Register must be R0-R7
| 16   |        |        | ;                                     |
| 17   |        |        | ; comment                             |
| 18   |        |        | ;                                     |
| 19   |        | 0x???? | GETCH                                 | Labels cannot be IN, OUT, GETC, or PUTS
| 20   | 0x0010 | 0x18E1 |     ADD R4, R3, #1      ; R4: 0x0001  |
| 21   | 0x0012 | 0x???? |     LDB R0, R0, #100                  | Offset required for this label is too large for this operand
| 22   | 0x0014 | 0xDB08 |     LSHF R5, R4, #8     ; R5: 0x0100  |
| 23   | 0x0016 | 0xDB54 |     RSHFL R5, R5, #4    ; R5: 0x0010  |
| 24   | 0x0018 | 0xDD4B |     LSHF R6, R5, #11    ; R6: 0x8000  |
| 25   | 0x001A | 0xDDB7 |     RSHFA R6, R6, #7    ; R6: 0xFF00  |
| 26   | 0x001C | 0x9182 |     XOR R0, R6, R2      ; R0: 0x00FF  |
| 27   | 0x001E | 0x???? |     ADD R4                            | Not enough operands for this instruction
| 28   | 0x0020 | 0x???? |     ADD R4, R4                        | Not enough operands for this instruction
| 29   |        | 0x???? |     BX LR                             | Invalid opcode
| 30   |        |        |                                       |
| 31   | 0x0022 | 0xF025 |     HALT                              |
| 32   |        |        |                                       |
| 33   | 0x0024 | 0x3000 | A   .FILL x3000                       |
| 34   |        |        |     .END                              |
| 35   |        |        |                                       |
| 36   |        |        |     LDB R0, R0, #1                    |
+------+--------+--------+---------------------------------------+

Found 9 errors:
+------+--------+--------+---------------------------------------+
| 2    |        | 0x???? |     ADD R0, R0, R2                    | Instructions cannot occur before .ORIG
+------+--------+--------+---------------------------------------+
| 4    |        | 0x???? |     .ORIG x3001                       | .ORIG is not word aligned
+------+--------+--------+---------------------------------------+
| 14   | 0x000C | 0x???? |     LDB R0, #2                        | Register must be R0-R7
+------+--------+--------+---------------------------------------+
| 15   | 0x000E | 0x???? |     LDW R12, R0, #0                   | Register must be R0-R7
+------+--------+--------+---------------------------------------+
| 19   |        | 0x???? | GETCH                                 | Labels cannot be IN, OUT, GETC, or PUTS
+------+--------+--------+---------------------------------------+
| 21   | 0x0012 | 0x???? |     LDB R0, R0, #100                  | Offset required for this label is too large for this operand
+------+--------+--------+---------------------------------------+
| 27   | 0x001E | 0x???? |     ADD R4                            | Not enough operands for this instruction
+------+--------+--------+---------------------------------------+
| 28   | 0x0020 | 0x???? |     ADD R4, R4                        | Not enough operands for this instruction
+------+--------+--------+---------------------------------------+
| 29   |        | 0x???? |     BX LR                             | Invalid opcode
+------+--------+--------+---------------------------------------+
```
