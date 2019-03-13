; Check condition codes
    .ORIG x3000
    AND R0, R0, #0
    ADD R0, R0, #1
    BRp S1
    BR WRONG
S1  BRnp S2
    BR WRONG
S2  BRzp S3
    BR WRONG
S3  BRnzp S4
    BR WRONG
S4  AND R0, R0, #0
    ADD R0, R0, #-1
    BRn S5
    BR WRONG
S5  LEA R5, WRONG   ; shouldn't set CC
    BRn S6
    BR WRONG
S6  AND R0, R0, #-1 ; should still be negative
    BRn S7
    BR WRONG
S7  LEA R0, Z
    LDW R0, R0, #0
    BRp S8
    BR WRONG
S8  NOT R0, R0
    BRn S9
    BR WRONG
S9  LEA R0, Z
    LDB R0, R0, #0
    BRn S10
    BR WRONG
S10 LEA R0, Z
    LDB R0, R0, #1
    BRz S11
    BR WRONG
S11 AND R1, R1, #0
    ADD R1, R1, #1
    HALT            ; Halt with success

WRONG
    AND R1, R1, #0
    ADD R1, R1, #-1
    HALT            ; Halt with error

Z   .FILL x00FF

    .END
