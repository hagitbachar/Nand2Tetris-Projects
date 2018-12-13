//push constant 7
@7
D=A
//SP = D
@SP
A=M
M=D
//SP++
@SP
M=M+1
//push constant 8
@8
D=A
//SP = D
@SP
A=M
M=D
//SP++
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=M+D
