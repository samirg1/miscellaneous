# Title:	Find the number of multiples of n in an array.
# Author:	Samir Gupta
# Date:		15/03/2022

	.data # store global variables
i:	.word 0
count:	.word 0 
n:	.word 0 
size:	.word 0
list:	.word 0
list_i:	.word 0
sizeP:	.asciiz "Enter array length : "
n_inpt:	.asciiz "Enter n : "
valueP:	.asciiz "Enter the value : "
final:	.asciiz "\nThe number of multiples (excluding itself) = "
newline:.asciiz "\n"

	.text
main:	la $a0, sizeP # print array size prompt
	addi $v0, $0, 4
	syscall
	
	addi $v0, $0, 5 # get integer value for size
	syscall
	sw $v0, size
	
	la $a0, n_inpt # print n prompt
	addi $v0, $0, 4
	syscall
	
	addi $v0, $0, 5 # get integer value for n
	syscall
	sw $v0, n
	
	# allocate space for array
	addi $v0, $0, 9 
	lw $t0, size 
	sll $t0, $t0, 2 
	addi $a0, $t0, 4 
	syscall # allocate space
	sw $v0, list
	sw $t0, ($v0) # $t0 = len
	
	sw $0, i 
loop:	# loop over array
	# determine whether to end loop
	lw $t0, i 
	lw $t1, size 
	slt $t2, $t0, $t1 # $t2 = 1 if i<size else 0
	beq $t2, $0, end # go to end if $t2 = 0 else continue
	
	# create list[i]
	lw $t0, i 
	lw $t1, list 
	la $a0, valueP
	addi $v0, $0, 4
	syscall  # print the value prompt
	sll $t0, $t0, 2 
	add $t0, $t0, $t1 # $a0 = address of list[i-1]
	addi $v0, $0, 5 # get item
	syscall
	sw $v0, 4($t0) # store item in allocated space for list[i]
	
	# get list[i]
	lw $t0, i 
	lw $t1, list 
	sll $t0, $t0, 2 
	add $t2, $t0, $t1 
	lw $t0, 4($t2) # $t0 = list[i]
	sw $t0, list_i # store list[o]
	
	# check if list[i] % n == 0
	lw $t0, list_i
	lw $t1, n # $t1 = n
	div $t0, $t1
	mfhi $t2
	bne $t2, $0, i_add # if list[i] % n != 0, branch to increment i
	
	# check if list[i] == n
	lw $t0, list_i # $t0 = list[i]
	lw $t1, n # $t1 = n
	beq $t0, $t1, i_add # if list[i] == n, branch to increment i
	
	# if code reaches this stage, list[i] % n == 0 and list[i] != n
	# increment count
	lw $t0, count # $t0 = count
	addi $t0, $t0, 1 # $t0 += 1
	sw $t0, count

i_add:	
    lw $t0, i # increment i
	addi $t0, $t0, 1
	sw $t0, i

	j loop	# loop

end:	
    la $a0, final # print the resulting text
	addi $v0, $0, 4
	syscall
	
	lw $a0, count # print the count
	addi $v0, $0, 1
	syscall
	
	la $a0, newline # print new line
	addi $v0, $0, 4
	syscall
	
	addi $v0, $0, 10 # exit
	syscall