//push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop to static8
@SP
AM=M-1
D=M
M=0
@StaticTest.8
M=D
//pop to static3
@SP
AM=M-1
D=M
M=0
@StaticTest.3
M=D
//pop to static1
@SP
AM=M-1
D=M
M=0
@StaticTest.1
M=D
//push static3
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
//push static1
@StaticTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=M-D
//push static8
@StaticTest.8
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=M+D
