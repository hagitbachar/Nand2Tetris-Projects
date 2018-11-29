// The program should sort the array starting at the address in R14 with length 
// as specified in R15. Don't change these registers.
// No assumptions can be made about the length of the array.
// You can assume that each value in the array (x) is -16384 < x < 16384.
// One can assume the array is allocated in the heap, meaning that the address in
// R14 is at least >= 2048, and that R14 + R15 <= 16383.
// The sort is in descending order - the largest number at the head of the array.



@R15 // the len of the array
D=M
@n
M=D // n = R0

@i
M=0 // i = 0

@j
M=0 //j = 0

(LOOP1)
	@i
	D=M
	@n
	D=D-M
	@STOP
	D;JGT // if i > n goto STOP
	

	(LOOP2)
		@j
		M=M+1
		D=M
		@n
		D=D-M
		@OUTLOOP2
		D;JGT // if  j > n go out from LOOP2
		@j
		D=M
		@R14 
		A=M+D // the address of a[j]
		D=M
		@R1 // we will put a[j] in R1
		M=D
		@i
		D=M
		@R14
		A=M+D // the address of a[i]
		D=M
		@R2 // we will put a[i] in R2
		M=D
		//check if a[i] > a[j], if so, goto swap
		@R1
		D=D-M
		@SWAP
		D;JGT
		@LOOP2 // if not, go to another iteration in LOOP2
		0;JMP


(SWAP)
	@i
	D=M
	@R14
	A=M+D // the address of a[i]
	D=A
	@R3
	M=D
	@j
	D=M
	@R14
	A=M+D // the address of a[j]
	D=A
	@R4
	M=D
	@R1 // a[j]
	D=M
	@R3
	A=M
	M=D // a[i] = a[j]

	@R2 // a[i]
	D=M
	@R4
	A=M
	M=D // a[j] = a[i]

	@LOOP2
	0;JMP
	


(OUTLOOP2)
	@i
	M=M+1 // i = 1 + 1
	D=M
	@j
	M=D
	@LOOP1  //go to another iteration in LOOP1
	0;JMP


(STOP)
	@STOP
	0;JMP


