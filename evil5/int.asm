.ORIG x1200

    ;Push R0
    ADD R6, R6, #-2
    STW R0, R6, #0
    ;Push R1
    ADD R6, R6, #-2
    STW R1, R6, #0
    ;Push R2
    ADD R6, R6, #-2
    STW R2, R6, #0

    LEA R0, TBL
    LDW R1, R0, #1
    LDW R0, R0, #0

LOOP LDW R2, R0, #0
    AND R2, R2, #-2
    STW R2, R0, #0
    ADD R0, R0, #2
    ADD R1, R1, #-1
    BRp LOOP

    ;Pop R2
    LDW R2, R6, #0
    ADD R6, R6, #2
    ;Pop R1
    LDW R1, R6, #0
    ADD R6, R6, #2
    ;Pop R0
    LDW R0, R6, #0
    ADD R6, R6, #2

    RTI
TBL .FILL x1000
    .FILL x0080

.END
