//push constant 3030
@3030
D=A
//SP = D
@SP
A=M
M=D
//SP++
@SP
M=M+1
//pop to pointer0
@SP
AM=M-1
D=M
M=0
@3
M=D
//push constant 3040
@3040
D=A
//SP = D
@SP
A=M
M=D
//SP++
@SP
M=M+1
//pop to pointer1
@SP
AM=M-1
D=M
M=0
@4
M=D
//push constant 32
@32
D=A
//SP = D
@SP
A=M
M=D
//SP++
@SP
M=M+1
//pop to this2
@2
D=A
@THIS
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D
//push constant 46
@46
D=A
//SP = D
@SP
A=M
M=D
//SP++
@SP
M=M+1
//pop to that6
@6
D=A
@THAT
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D
//push pointer0
@3
D=M
//SP = D
@SP
A=M
M=D
//SP++
@SP
M=M+1
//push pointer1
@4
D=M
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
//push this2
@2
D=A
@THIS
A=M+D
D=M//SP = D
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
M=M-D
//push that6
@6
D=A
@THAT
A=M+D
D=M//SP = D
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
