; Check memory instructions
    .ORIG x3000
    BR skip
A   .FILL x1234
B   .FILL x5678
C   .FILL x9ABC
D   .FILL xDEF0

skip LEA R0, B       ; R0=x3004
    LDW R1, R0, #-1 ; R1=x1234
    LDW R2, R0, #0  ; R2=x5678
    LDW R3, R0, #2  ; R3=xDEF0

    LDB R4, R0, #0  ; R4=x__78
    LDB R5, R0, #1  ; R5=x__56
    LDB R6, R0, #-2 ; R6=x__34

    AND R1, R1, #0
    ADD R1, R1, #15
    LEA R0, D
    STW R1, R0, #0  ; [x3008]=0x000F
    STW R1, R0, #-1 ; [x3006]=0x000F
    STB R1, R0, #2  ; [x3008]=0x??0F
    STB R1, R0, #-4 ; [x3004]=0x560F

    HALT
    .END