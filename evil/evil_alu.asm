; check ALU instructions
    .ORIG x3000
    
    AND R0, R0, #0
    ADD R0, R0, #5      ; R0: 0x0005
    ADD R1, R0, #-10    ; R1: 0xFFFB
    AND R2, R2, #0
    ADD R2, R2, #-1     ; R2: 0xFFFF
    NOT R3, R2          ; R3: 0x0000
    ADD R4, R3, #1      ; R4: 0x0001
    LSHF R5, R4, #8     ; R5: 0x0100
    RSHFL R5, R5, #4    ; R5: 0x0010
    LSHF R6, R5, #11    ; R6: 0x8000
    RSHFA R7, R6, #7    ; R7: 0xFF00
    XOR R0, R7, R2      ; R0: 0x00FF
    RSHFL R6, R6, #7    ; R6: 0x0100

    HALT                ; Ending: 00FF FFFB FFFF 0000 0001 0010 0100 FF00

    .END
