.ORIG x1200
	; Push R0, R1
	ADD R6, R6, #-2
	STW R0, R6, #0
	ADD R6, R6, #-2
	STW R1, R6, #0
	
	; R0 <- x4000
	LEA R0, TGT, #0
	LDW R0, R0, #0

	; [x4000] <- [x4000] + 2
	LDW R1, R0, #0
	ADD R1, R1, #1
	STW R1, R0, #0

	; Pop R0, R1
	LDW R1, R6, #0
	ADD R6, R6, #2
	LDW R0, R6, #0
	ADD R6, R6, #2

	RTI

TGT	.FILL x4000
.END
