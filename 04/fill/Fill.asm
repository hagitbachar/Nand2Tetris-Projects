// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(START)
	@SCREEN  // the first register of  the screen
	D=M
	@currentRegister
	M=D

	@8192 // num of registers to paint
	D=M
	@numRegisterToPaint
	M=D

	@KBD
	D=M
	@WHITE
	D;JEQ // if no press -> keyboard equal to zero, set all pixels to black
	@BLACK
	D;JNE // if press -> keyboard not equal to zero, set all pixels to white


(BLACK)
	@color
	M=-1
	@PAINT
	0;JMP
	
(WHITE)
	@color
	M=0
	@PAINT
	0;JMP	


(PAINT)
	@color
	D=M
	@currentRegister
	M=D
	M=M+1 // in the next iteration we will paint the next register

	@numRegisterToPaint
	M=M-1
	D=M
	@START
	D;JEQ // if all the registers are painted, we finish to paint, goto start
	

	@PAINT // else, go to the next itaration
	0;JMP
