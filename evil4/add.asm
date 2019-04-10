.ORIG x3000

		; [x4000] <- 1
		LEA R4, TGT, #0
		LDW R0, R4, #0
		AND R1, R1, #0
		ADD R1, R1, #1
		STW R1, R0, #0

		; Add
		LDW R0, R4, #1

		AND R2, R2, #0	; R2 is sum
		AND R3, R3, #0	; R3 is accumulator
		ADD R3, R3, #10
		ADD R3, R3, #10

LOOP	LDB R1, R0, #0
		ADD R2, R2, R1
		ADD R0, R0, #1
		ADD R3, R3, #-1
		BRp LOOP

		; Save
		LDW R0, R4, #2
		STW R2, R0, #0

		; Check
		LEA R4, TGT, #0
		LDW R0, R4, #0
		LDW R5, R0, #0 ; R5 = [0x4000] = 0x0002
		LDW R0, R4, #2
		LDw R4, R0, #0 ; R4 = sum = 0x0052

		TRAP x25

TGT		.FILL x4000
		.FILL xC000
		.FILL xC014 ; change this address to test exceptions

.END
