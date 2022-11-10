# Title :   Insertion sort algorithm
# Authors : Samir Gupta
# Date :    25/03/2022
		
	.data # global strings
newLine: .asciiz "\n"
space:	 .asciiz " "
	
	.text
	
	.globl main
	.globl insertion_sort
	
main:   
    # -4($fp) = address
	# -8($fp) = i

	# set the frame point to stack pointer ( $fp to $sp )
	addi $fp, $sp, 0
	
	# allocate space for local variable (pointer to array)
	addi $sp, $sp, -4
	
	# allocate space for array of length 5
	addi $v0, $0, 9 
	addi $t0, $0, 5
	sll $t1, $t0, 2
	addi $a0, $t1, 4 
	syscall
	sw $v0, -4($fp) 
	sw $t0, ($v0) # length of array is stored at first spot in array
	
	# settings elements of the array
	lw $t0, -4($fp) 
	
	addi $t1, $0, 6 # the_list[0]
	sw $t1, 4($t0)
	
	addi $t1, $0, -2 # the_list[1]
	sw $t1, 8($t0) 
	
	addi $t1, $0, 7 # the_list[2]
	sw $t1, 12($t0)
	
	addi $t1, $0, 4 # the_list[3]
	sw $t1, 16($t0)
	
	addi $t1, $0, -10 # the_list[4]
	sw $t1, 20($t0)
	
	# create space for argument
	addi $sp, $sp, -4	
	
	# load address as argument
	lw $t0, -4($fp) 
	sw $t0, 0($sp)
	
	jal insertion_sort
	
	# deallocate argument
	addi $sp, $sp, 4
	
	# allocate space for local
	addi $sp, $sp, -4
	
	# store i as the local
	sw $0, -8($fp)
main_loop:
	# check if i < len(the_list)
	lw $t0, -8($fp) # $t0 = i
	lw $t1, -4($fp)
	lw $t1, ($t1)	# $t1 = length of array
	slt $t2, $t0, $t1 
	beq $t2, $0, end_main # go to end if !(i < len(the_list))
	
	# print list[i]
	lw $t0, -8($fp) # $t0 = i
	lw $t1, -4($fp) 
	sll $t0, $t0, 2
	add $t2, $t0, $t1
	lw $a0, 4($t2) # load list[i] into $t0
	addi $v0, $0,1
	syscall # print list[i]
	
	# print space
	la $a0, space
	addi $v0, $0, 4
	syscall
	
	# increment i
	lw $t0, -8($fp)
	addi $t0, $t0, 1
	sw $t0, -8($fp)
	
	j main_loop
	
end_main:
	# print newline
    la $a0, newLine
    add $v0, $0, 4
    syscall

    # exit
    addi $v0, $0, 10
    syscall
	
insertion_sort: 
	# address = 8($fp)
	# $ra = 4(fp)
	# $fp = 0($fp)
	# i = -4($fp)
	# key = -8($fp)
	# j = -12($fp)
	# length of array = -16($fp)

	# store ra and fp on the stack 
    addi $sp, $sp, -4	
    sw $ra, ($sp)
    addi $sp, $sp, -4
    sw $fp, ($sp)
	
	# copy $sp to $fp
	addi $fp, $sp, 0
	
	# allocate space for 4 locals
	addi $sp, $sp, -16
	
	# store i
	addi $t0, $0, 1
	sw $t0, -4($fp) 
	
	# store key
	sw $0, -8($fp)
	
	# store j
	sw $0, -12($fp)
	
	# store length
	lw $t0, 8($fp)
	lw $t0, ($t0)
	sw $t0, -16($fp)
	
for_loop: # loop over array
	
	# check if i < len(the_list) 
	lw $t0, -4($fp) # $t0 = i
	lw $t1, -16($fp)
	slt $t2, $t0, $t1 
	beq $t2, $0, end_for # go to end if !(i < len(the_list))
	
	# set key = list[i]
	lw $t0, -4($fp)
	lw $t1, 8($fp) 
	sll $t0, $t0, 2 
	add $t2, $t0, $t1 
	lw $t0, 4($t2) # $t0 = list[i]
	sw $t0, -8($fp) # key = list[i]
	
	# j = i-1
	lw $t0, -4($fp)
	addi $t0, $t0, -1 
	sw $t0, -12($fp)
	
	
while_loop:
	# j >= 0 condition
	lw $t0, -12($fp) # $t0 = j
	slt $t2, $t0, $0 
	bne $t2, $0, end_while # go to end_while if j < 0
	
	# key < the_list[j] condition
	lw $t0, -12($fp) # $t0 = j
	lw $t1, 8($fp) 
	sll $t0, $t0, 2
	add $t2, $t0, $t1 
	lw $t0, 4($t2) # $t0 = the_list[j]
	lw $t3, -8($fp) # $t3 = key
	slt $t2, $t3, $t0
	beq $t2, $0, end_while # go to end_while if not(the_list[j] < key) else continue
	
	
	# the_list[j+1] = the_list[j]
	lw $t0, -12($fp) # $t0 = j
	lw $t1, 8($fp) 
	sll $t0, $t0, 2 
	add $t2, $t0, $t1 
	lw $t0, 4($t2) # $t0 = list[j]
	sw $t0, 8($t2) # list [j+1] = $t0 (list[j])
	
	# decrement j
	lw $t0, -12($fp)
	addi $t0, $t0, -1
	sw $t0, -12($fp)
	
	j while_loop
	
	
end_while:
	# the_list[j+1] = key
	lw $t0, -12($fp) # $t0 = j
	lw $t1, 8($fp) 
	sll $t0, $t0, 2
	add $t2, $t0, $t1 
	lw $t3, -8($fp)	# $t3 = key
	sw $t3, 8($t2) # list [j+1] = $t3
	
	# increment i
	lw $t0, -4($fp) # $t0 = i
	addi $t0, $t0, 1
	sw $t0, -4($fp)
	
	j for_loop
	
end_for:
	# deallocate locals vars (i, j, len, and key)
	addi $sp, $sp, 16
	
	# jump back to main
	lw $fp, 0($sp)
	lw $ra, 4($sp)
	addi $sp, $sp, 8
	jr $ra