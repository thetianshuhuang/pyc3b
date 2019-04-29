# pyc3b

Python LC3b Assembler

![](https://github.com/thetianshuhuang/pyc3b/blob/master/preview/assembler.png)

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

***

# lc3test

Python LC3b Simulator test engine -- for EE460N Lab 2-6 (Yale Patt, UT Austin)

![](https://github.com/thetianshuhuang/pyc3b/blob/master/preview/tester.png)

## Dependencies
- Python 3
- [print](https://github.com/thetianshuhuang/print)

## Usage
1. Copy ```evil/``` to the simulator directory.
2. Compile the simlulator to ```a.out```.
3. Use the modified ```__header__.h``` instead of the provided one; a ```#DEBUG_MODE``` flag has been added that should be enabled in order to interface with the test engine. [ctp](https://github.com/thetianshuhuang/ctp) is recommended in order to manage source files.
4. Run the tester:
```shell
$ python tester.py [-flags]
```
5. Comments can be passed through to the tester by leading them with a ```#```. DO NOT add other ```printf``` statements (this will mess up the parser). For example:
```
printf("# Debug Value: %0.4x\n", debug_variable);
```


## Flags:
- ```-c```, ```--csv```: Format output as CSV
- ```--all```: Run all tests
- ```--alu```, ```--cc```, ```--jmp```, ```--memory```, ```--add```: Run specific test case. **NOTE**: ```--add``` is only supported for labs 4 and 5 (```-4```, ```-5```)
- ```-3```, ```-4```, ```-5```: Specify target lab; defaults to 3
- ```--getcmd``` (```-g```): Get command to use with vanilla tool instead of running the tester
- ```--ins``` (```-i```): Show instructions only (don't elaborate on clocks within each instruction)
- ```--nc``` (```-c```): Hide comments
- ```--noint``` (```-n```): Hide ISR (int.asm) (since it takes up ~25k cycles)


# Sample Sessions
## Assembler
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

## Tester
```
$: python tester.py --alu

     _    ___ _____      _____       _
    | |  / __|__ / |__  |_   _|__ __| |_ ___ _ _
    | |_| (__ |_ \ '_ \   | |/ -_|_-<  _/ -_) '_|
    |____\___|___/_.__/   |_|\___/__/\__\___|_|
    LC3b Clock-Level Simulator Test Engine
    Tianshu Huang, Spring 2019 -- EE 460N @ UT Austin (Yale Patt)


       [evil_alu]

-003-  pc: 0x3000  ir: 0x5020  src: "AND R0, R0, #0"
[000]  pc: 0x3000  ir: 0x0000  st: 18  bus: 0x0000  mdr: 0x0000  mar: 0x0000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[001]  pc: 0x3002  ir: 0x0000  st: 33  bus: 0x3000  mdr: 0x0000  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[002]  pc: 0x3002  ir: 0x0000  st: 33  bus: 0x0000  mdr: 0x0000  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[003]  pc: 0x3002  ir: 0x0000  st: 33  bus: 0x0000  mdr: 0x0000  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[004]  pc: 0x3002  ir: 0x0000  st: 33  bus: 0x0000  mdr: 0x0000  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[005]  pc: 0x3002  ir: 0x0000  st: 33  bus: 0x0000  mdr: 0x5020  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[006]  pc: 0x3002  ir: 0x0000  st: 35  bus: 0x0000  mdr: 0x5020  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[007]  pc: 0x3002  ir: 0x5020  st: 32  bus: 0x5020  mdr: 0x5020  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[008]  pc: 0x3002  ir: 0x5020  st: 05  bus: 0x0000  mdr: 0x5020  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
-004-  pc: 0x3002  ir: 0x1025  src: "ADD R0, R0, #5"
[009]  pc: 0x3002  ir: 0x5020  st: 18  bus: 0x0000  mdr: 0x5020  mar: 0x3000  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[010]  pc: 0x3004  ir: 0x5020  st: 33  bus: 0x3002  mdr: 0x5020  mar: 0x3002  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[011]  pc: 0x3004  ir: 0x5020  st: 33  bus: 0x0000  mdr: 0x5020  mar: 0x3002  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[012]  pc: 0x3004  ir: 0x5020  st: 33  bus: 0x0000  mdr: 0x5020  mar: 0x3002  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[013]  pc: 0x3004  ir: 0x5020  st: 33  bus: 0x0000  mdr: 0x5020  mar: 0x3002  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[014]  pc: 0x3004  ir: 0x5020  st: 33  bus: 0x0000  mdr: 0x1025  mar: 0x3002  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[015]  pc: 0x3004  ir: 0x5020  st: 35  bus: 0x0000  mdr: 0x1025  mar: 0x3002  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[016]  pc: 0x3004  ir: 0x1025  st: 32  bus: 0x1025  mdr: 0x1025  mar: 0x3002  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
[017]  pc: 0x3004  ir: 0x1025  st: 01  bus: 0x0000  mdr: 0x1025  mar: 0x3002  nzp: 010  reg: 0000 0000 0000 0000 0000 0000 0000 0000
-005-  pc: 0x3004  ir: 0x1236  src: "ADD R1, R0, #-10"
[018]  pc: 0x3004  ir: 0x1025  st: 18  bus: 0x0005  mdr: 0x1025  mar: 0x3002  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
[019]  pc: 0x3006  ir: 0x1025  st: 33  bus: 0x3004  mdr: 0x1025  mar: 0x3004  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
[020]  pc: 0x3006  ir: 0x1025  st: 33  bus: 0x0000  mdr: 0x1025  mar: 0x3004  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
[021]  pc: 0x3006  ir: 0x1025  st: 33  bus: 0x0000  mdr: 0x1025  mar: 0x3004  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
[022]  pc: 0x3006  ir: 0x1025  st: 33  bus: 0x0000  mdr: 0x1025  mar: 0x3004  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
[023]  pc: 0x3006  ir: 0x1025  st: 33  bus: 0x0000  mdr: 0x1236  mar: 0x3004  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
[024]  pc: 0x3006  ir: 0x1025  st: 35  bus: 0x0000  mdr: 0x1236  mar: 0x3004  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
[025]  pc: 0x3006  ir: 0x1236  st: 32  bus: 0x1236  mdr: 0x1236  mar: 0x3004  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
[026]  pc: 0x3006  ir: 0x1236  st: 01  bus: 0x0000  mdr: 0x1236  mar: 0x3004  nzp: 001  reg: 0005 0000 0000 0000 0000 0000 0000 0000
-006-  pc: 0x3006  ir: 0x54A0  src: "AND R2, R2, #0"
[027]  pc: 0x3006  ir: 0x1236  st: 18  bus: 0xFFFB  mdr: 0x1236  mar: 0x3004  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[028]  pc: 0x3008  ir: 0x1236  st: 33  bus: 0x3006  mdr: 0x1236  mar: 0x3006  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[029]  pc: 0x3008  ir: 0x1236  st: 33  bus: 0x0000  mdr: 0x1236  mar: 0x3006  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[030]  pc: 0x3008  ir: 0x1236  st: 33  bus: 0x0000  mdr: 0x1236  mar: 0x3006  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[031]  pc: 0x3008  ir: 0x1236  st: 33  bus: 0x0000  mdr: 0x1236  mar: 0x3006  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[032]  pc: 0x3008  ir: 0x1236  st: 33  bus: 0x0000  mdr: 0x54A0  mar: 0x3006  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[033]  pc: 0x3008  ir: 0x1236  st: 35  bus: 0x0000  mdr: 0x54A0  mar: 0x3006  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[034]  pc: 0x3008  ir: 0x54A0  st: 32  bus: 0x54A0  mdr: 0x54A0  mar: 0x3006  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[035]  pc: 0x3008  ir: 0x54A0  st: 05  bus: 0x0000  mdr: 0x54A0  mar: 0x3006  nzp: 100  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
-007-  pc: 0x3008  ir: 0x14BF  src: "ADD R2, R2, #-1"
[036]  pc: 0x3008  ir: 0x54A0  st: 18  bus: 0x0000  mdr: 0x54A0  mar: 0x3006  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[037]  pc: 0x300A  ir: 0x54A0  st: 33  bus: 0x3008  mdr: 0x54A0  mar: 0x3008  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[038]  pc: 0x300A  ir: 0x54A0  st: 33  bus: 0x0000  mdr: 0x54A0  mar: 0x3008  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[039]  pc: 0x300A  ir: 0x54A0  st: 33  bus: 0x0000  mdr: 0x54A0  mar: 0x3008  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[040]  pc: 0x300A  ir: 0x54A0  st: 33  bus: 0x0000  mdr: 0x54A0  mar: 0x3008  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[041]  pc: 0x300A  ir: 0x54A0  st: 33  bus: 0x0000  mdr: 0x14BF  mar: 0x3008  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[042]  pc: 0x300A  ir: 0x54A0  st: 35  bus: 0x0000  mdr: 0x14BF  mar: 0x3008  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[043]  pc: 0x300A  ir: 0x14BF  st: 32  bus: 0x14BF  mdr: 0x14BF  mar: 0x3008  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
[044]  pc: 0x300A  ir: 0x14BF  st: 01  bus: 0x0000  mdr: 0x14BF  mar: 0x3008  nzp: 010  reg: 0005 FFFB 0000 0000 0000 0000 0000 0000
-008-  pc: 0x300A  ir: 0x96BF  src: "NOT R3, R2"
[045]  pc: 0x300A  ir: 0x14BF  st: 18  bus: 0xFFFF  mdr: 0x14BF  mar: 0x3008  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[046]  pc: 0x300C  ir: 0x14BF  st: 33  bus: 0x300A  mdr: 0x14BF  mar: 0x300A  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[047]  pc: 0x300C  ir: 0x14BF  st: 33  bus: 0x0000  mdr: 0x14BF  mar: 0x300A  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[048]  pc: 0x300C  ir: 0x14BF  st: 33  bus: 0x0000  mdr: 0x14BF  mar: 0x300A  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[049]  pc: 0x300C  ir: 0x14BF  st: 33  bus: 0x0000  mdr: 0x14BF  mar: 0x300A  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[050]  pc: 0x300C  ir: 0x14BF  st: 33  bus: 0x0000  mdr: 0x96BF  mar: 0x300A  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[051]  pc: 0x300C  ir: 0x14BF  st: 35  bus: 0x0000  mdr: 0x96BF  mar: 0x300A  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[052]  pc: 0x300C  ir: 0x96BF  st: 32  bus: 0x96BF  mdr: 0x96BF  mar: 0x300A  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[053]  pc: 0x300C  ir: 0x96BF  st: 09  bus: 0x0000  mdr: 0x96BF  mar: 0x300A  nzp: 100  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
-009-  pc: 0x300C  ir: 0x18E1  src: "ADD R4, R3, #1"
[054]  pc: 0x300C  ir: 0x96BF  st: 18  bus: 0x0000  mdr: 0x96BF  mar: 0x300A  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[055]  pc: 0x300E  ir: 0x96BF  st: 33  bus: 0x300C  mdr: 0x96BF  mar: 0x300C  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[056]  pc: 0x300E  ir: 0x96BF  st: 33  bus: 0x0000  mdr: 0x96BF  mar: 0x300C  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[057]  pc: 0x300E  ir: 0x96BF  st: 33  bus: 0x0000  mdr: 0x96BF  mar: 0x300C  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[058]  pc: 0x300E  ir: 0x96BF  st: 33  bus: 0x0000  mdr: 0x96BF  mar: 0x300C  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[059]  pc: 0x300E  ir: 0x96BF  st: 33  bus: 0x0000  mdr: 0x18E1  mar: 0x300C  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[060]  pc: 0x300E  ir: 0x96BF  st: 35  bus: 0x0000  mdr: 0x18E1  mar: 0x300C  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[061]  pc: 0x300E  ir: 0x18E1  st: 32  bus: 0x18E1  mdr: 0x18E1  mar: 0x300C  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
[062]  pc: 0x300E  ir: 0x18E1  st: 01  bus: 0x0000  mdr: 0x18E1  mar: 0x300C  nzp: 010  reg: 0005 FFFB FFFF 0000 0000 0000 0000 0000
-010-  pc: 0x300E  ir: 0xDB08  src: "LSHF R5, R4, #8"
[063]  pc: 0x300E  ir: 0x18E1  st: 18  bus: 0x0001  mdr: 0x18E1  mar: 0x300C  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
[064]  pc: 0x3010  ir: 0x18E1  st: 33  bus: 0x300E  mdr: 0x18E1  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
[065]  pc: 0x3010  ir: 0x18E1  st: 33  bus: 0x0000  mdr: 0x18E1  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
[066]  pc: 0x3010  ir: 0x18E1  st: 33  bus: 0x0000  mdr: 0x18E1  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
[067]  pc: 0x3010  ir: 0x18E1  st: 33  bus: 0x0000  mdr: 0x18E1  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
[068]  pc: 0x3010  ir: 0x18E1  st: 33  bus: 0x0000  mdr: 0xDB08  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
[069]  pc: 0x3010  ir: 0x18E1  st: 35  bus: 0x0000  mdr: 0xDB08  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
[070]  pc: 0x3010  ir: 0xDB08  st: 32  bus: 0xDB08  mdr: 0xDB08  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
[071]  pc: 0x3010  ir: 0xDB08  st: 13  bus: 0x0000  mdr: 0xDB08  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0000 0000 0000
-011-  pc: 0x3010  ir: 0xDB54  src: "RSHFL R5, R5, #4"
[072]  pc: 0x3010  ir: 0xDB08  st: 18  bus: 0x0100  mdr: 0xDB08  mar: 0x300E  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
[073]  pc: 0x3012  ir: 0xDB08  st: 33  bus: 0x3010  mdr: 0xDB08  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
[074]  pc: 0x3012  ir: 0xDB08  st: 33  bus: 0x0000  mdr: 0xDB08  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
[075]  pc: 0x3012  ir: 0xDB08  st: 33  bus: 0x0000  mdr: 0xDB08  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
[076]  pc: 0x3012  ir: 0xDB08  st: 33  bus: 0x0000  mdr: 0xDB08  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
[077]  pc: 0x3012  ir: 0xDB08  st: 33  bus: 0x0000  mdr: 0xDB54  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
[078]  pc: 0x3012  ir: 0xDB08  st: 35  bus: 0x0000  mdr: 0xDB54  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
[079]  pc: 0x3012  ir: 0xDB54  st: 32  bus: 0xDB54  mdr: 0xDB54  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
[080]  pc: 0x3012  ir: 0xDB54  st: 13  bus: 0x0000  mdr: 0xDB54  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0100 0000 0000
-012-  pc: 0x3012  ir: 0xDD4B  src: "LSHF R6, R5, #11"
[081]  pc: 0x3012  ir: 0xDB54  st: 18  bus: 0x0010  mdr: 0xDB54  mar: 0x3010  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
[082]  pc: 0x3014  ir: 0xDB54  st: 33  bus: 0x3012  mdr: 0xDB54  mar: 0x3012  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
[083]  pc: 0x3014  ir: 0xDB54  st: 33  bus: 0x0000  mdr: 0xDB54  mar: 0x3012  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
[084]  pc: 0x3014  ir: 0xDB54  st: 33  bus: 0x0000  mdr: 0xDB54  mar: 0x3012  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
[085]  pc: 0x3014  ir: 0xDB54  st: 33  bus: 0x0000  mdr: 0xDB54  mar: 0x3012  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
[086]  pc: 0x3014  ir: 0xDB54  st: 33  bus: 0x0000  mdr: 0xDD4B  mar: 0x3012  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
[087]  pc: 0x3014  ir: 0xDB54  st: 35  bus: 0x0000  mdr: 0xDD4B  mar: 0x3012  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
[088]  pc: 0x3014  ir: 0xDD4B  st: 32  bus: 0xDD4B  mdr: 0xDD4B  mar: 0x3012  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
[089]  pc: 0x3014  ir: 0xDD4B  st: 13  bus: 0x0000  mdr: 0xDD4B  mar: 0x3012  nzp: 001  reg: 0005 FFFB FFFF 0000 0001 0010 0000 0000
-013-  pc: 0x3014  ir: 0xDDB7  src: "RSHFA R6, R6, #7"
[090]  pc: 0x3014  ir: 0xDD4B  st: 18  bus: 0x8000  mdr: 0xDD4B  mar: 0x3012  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
[091]  pc: 0x3016  ir: 0xDD4B  st: 33  bus: 0x3014  mdr: 0xDD4B  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
[092]  pc: 0x3016  ir: 0xDD4B  st: 33  bus: 0x0000  mdr: 0xDD4B  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
[093]  pc: 0x3016  ir: 0xDD4B  st: 33  bus: 0x0000  mdr: 0xDD4B  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
[094]  pc: 0x3016  ir: 0xDD4B  st: 33  bus: 0x0000  mdr: 0xDD4B  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
[095]  pc: 0x3016  ir: 0xDD4B  st: 33  bus: 0x0000  mdr: 0xDDB7  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
[096]  pc: 0x3016  ir: 0xDD4B  st: 35  bus: 0x0000  mdr: 0xDDB7  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
[097]  pc: 0x3016  ir: 0xDDB7  st: 32  bus: 0xDDB7  mdr: 0xDDB7  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
[098]  pc: 0x3016  ir: 0xDDB7  st: 13  bus: 0x0000  mdr: 0xDDB7  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 8000 0000
-014-  pc: 0x3016  ir: 0x9182  src: "XOR R0, R6, R2"
[099]  pc: 0x3016  ir: 0xDDB7  st: 18  bus: 0xFF00  mdr: 0xDDB7  mar: 0x3014  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
[100]  pc: 0x3018  ir: 0xDDB7  st: 33  bus: 0x3016  mdr: 0xDDB7  mar: 0x3016  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
[101]  pc: 0x3018  ir: 0xDDB7  st: 33  bus: 0x0000  mdr: 0xDDB7  mar: 0x3016  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
[102]  pc: 0x3018  ir: 0xDDB7  st: 33  bus: 0x0000  mdr: 0xDDB7  mar: 0x3016  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
[103]  pc: 0x3018  ir: 0xDDB7  st: 33  bus: 0x0000  mdr: 0xDDB7  mar: 0x3016  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
[104]  pc: 0x3018  ir: 0xDDB7  st: 33  bus: 0x0000  mdr: 0x9182  mar: 0x3016  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
[105]  pc: 0x3018  ir: 0xDDB7  st: 35  bus: 0x0000  mdr: 0x9182  mar: 0x3016  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
[106]  pc: 0x3018  ir: 0x9182  st: 32  bus: 0x9182  mdr: 0x9182  mar: 0x3016  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
[107]  pc: 0x3018  ir: 0x9182  st: 09  bus: 0x0000  mdr: 0x9182  mar: 0x3016  nzp: 100  reg: 0005 FFFB FFFF 0000 0001 0010 FF00 0000
-016-  pc: 0x3018  ir: 0xF025  src: "HALT "
[108]  pc: 0x3018  ir: 0x9182  st: 18  bus: 0x00FF  mdr: 0x9182  mar: 0x3016  nzp: 001  reg: 00FF FFFB FFFF 0000 0001 0010 FF00 0000
[109]  pc: 0x301A  ir: 0x9182  st: 33  bus: 0x3018  mdr: 0x9182  mar: 0x3018  nzp: 001  reg: 00FF FFFB FFFF 0000 0001 0010 FF00 0000
[110]  pc: 0x301A  ir: 0x9182  st: 33  bus: 0x0000  mdr: 0x9182  mar: 0x3018  nzp: 001  reg: 00FF FFFB FFFF 0000 0001 0010 FF00 0000
[111]  pc: 0x301A  ir: 0x9182  st: 33  bus: 0x0000  mdr: 0x9182  mar: 0x3018  nzp: 001  reg: 00FF FFFB FFFF 0000 0001 0010 FF00 0000
[112]  pc: 0x301A  ir: 0x9182  st: 33  bus: 0x0000  mdr: 0x9182  mar: 0x3018  nzp: 001  reg: 00FF FFFB FFFF 0000 0001 0010 FF00 0000
[113]  pc: 0x301A  ir: 0x9182  st: 33  bus: 0x0000  mdr: 0xF025  mar: 0x3018  nzp: 001  reg: 00FF FFFB FFFF 0000 0001 0010 FF00 0000
[114]  pc: 0x301A  ir: 0x9182  st: 35  bus: 0x0000  mdr: 0xF025  mar: 0x3018  nzp: 001  reg: 00FF FFFB FFFF 0000 0001 0010 FF00 0000
```
