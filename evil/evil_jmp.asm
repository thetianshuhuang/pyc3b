; Branch, JMP, Subroutines
; R1=1: A called
; R1=2: B called
; R1=-1: overran function end
    .ORIG x3000

    LEA R7, S
    BR A            ; R1=1
S   JSR B           ; R1=2
    LEA R7, C       ; program should halt
    JMP R7

A   AND R1, R1, #0
    ADD R1, R1, #1
    RET
    AND R1, R1, #0
    ADD R1, R1, #-1

B   AND R1, R1, #0
    ADD R1, R1, #2
    RET
    AND R1, R1, #0
    ADD R1, R1, #-1

C   AND R1, R1, #0
    ADD R1, R1, #3
    HALT
    .END
