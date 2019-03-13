; Branch, JMP, Subroutines
; R1=1: A called
; R1=2: B called
; R1=-1: overran function end
    .ORIG x3000

    LEA R7, S
    BR A            ; R1=1
S   JSR B           ; R2=2
    LEA R7, C       ; R3=3; program should halt
    JMP R7

A   AND R1, R1, #0
    ADD R1, R1, #1
    RET
    AND R1, R1, #0
    ADD R1, R1, #-1

B   AND R2, R2, #0
    ADD R2, R2, #2
    RET
    AND R1, R1, #0
    ADD R1, R1, #-1

C   AND R3, R3, #0
    ADD R3, R3, #3
    HALT            ; If all calls correct, R1=1, R2=2, R3=3
    .END
