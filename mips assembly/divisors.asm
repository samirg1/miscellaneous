# Title:    Find divisors of two numbers.
# Author:   Samir Gupta
# Date:     14/03/2022
	
	.data # store global variables
number_label:	.asciiz "Enter the number: "
firstDivisor_label:	.asciiz "Enter the first divisor: "
secondDivisor_label:	.asciiz "Enter the second divisor: "
divisor_label:	.asciiz "\nDivisors: "
divisor:	.word 0
number:	.word 0
firstDivisor:	.word 0
secondDivisor:	.word 0
firstTrue:	.word 0
secondTrue:	.word 0
newline:	.asciiz "\n"

        .text
main:       
	# print number_label
	la $a0 , number_label
	addi $v0, $0, 4
	syscall
	
	# read the number
	addi $v0, $0, 5
	syscall
	sw $v0, number
	
	# print firstDivisor_label
	la $a0 , firstDivisor_label
	addi $v0, $0, 4
	syscall
	
	# read the divisor
	addi $v0, $0, 5
	syscall
	sw $v0, firstDivisor
	
	# print secondDivisor_label
	la $a0 , secondDivisor_label
	addi $v0, $0, 4
	syscall
	
	# read the divisor
	addi $v0, $0, 5
	syscall
	sw $v0, secondDivisor
	
	# is first remainder < 1 ?
	lw $t0, number 
	lw $t1, firstDivisor
	lw $t2, secondDivisor
	div $t0, $t1
	mfhi $t0	
	slti $t0, $t0, 1
	sw $t0, firstTrue
	
	# is second remainder < 1 ?
	lw $t0, number 
	lw $t1, firstDivisor
	lw $t2, secondDivisor 
	div $t0, $t2
	mfhi $t0
	slti $t0, $t0, 1
	sw $t0, secondTrue
	
	# go to elif if not (both remainders are less than 1)
	lw $t0, firstTrue
	lw $t1, secondTrue
	and $t0, $t0, $t1
	beq $t0, $0, elif
	    
	 # if both are true store divisor = 2
	 addi $t0, $0, 2
	 sw $t0, divisor
	 
	 j endif # skip to end
 	
elif: 	   
	# go to else if neither remainders are less than 1
	lw $t0, firstTrue
	lw $t1, secondTrue 
	or $t0, $t0, $t1
	beq $t0, $0, else

	# if one remainder is less than 1, store divisors = 1
	addi $t0, $0, 1
	sw $t0, divisor
	
	j endif # skip to end
    
else:	
	# if neither remainders are less than 1, store divisors = 0
	addi $t0, $0, 0	
	sw $t0, divisor
	    
endif:
	# print divisor_label
	la $a0, divisor_label
	addi $v0, $0, 4
	syscall
	
	# print divisor
	lw $a0, divisor
	addi $v0, $0, 1
	syscall
	
	# print newline
	la $a0, newline
	addi $v0, $0, 4
	syscall
	
	# exit
	addi $v0, $0, 10
	syscall