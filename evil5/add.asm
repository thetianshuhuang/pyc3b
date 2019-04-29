.ORIG x3000

        ; [x4000] <- 1
        LEA R4, TGT

        ; Add
        LDW R0, R4, #1

        AND R2, R2, #0
        AND R3, R3, #0
        ADD R3, R3, #10
        ADD R3, R3, #10

LOOP    LDB R1, R0, #0
        ADD R2, R2, R1
        ADD R0, R0, #1
        ADD R3, R3, #-1
        BRp LOOP

        ; Save
        LDW R0, R4, #2
        STW R2, R0, #0

        JMP R2
        ; TRAP x25

TGT     .FILL x4000
        .FILL xC000
        .FILL xC014

.END
