# Title:	Find the amount of multiples of a number.
# Author:	Samir Gupta
# Date:		15/03/2022

	.data
final:	.asciiz "\nThe number of multiples of "
is:	.asciiz " is: "

	.text

	.globl main
	.globl get_multiples

main:
    # array address = -4($fp)
    # n = -8($fp)

	# copy $sp to $fp to make space for locals
	addi $fp, $sp, 0 # copy stack pointer to frame pointer

    # make space for locals
	addi $sp, $sp, -8 # move stack pointer up 8 bytes, to make spapce for my_list and n.
	
	# allocating space for the array
	addi $v0, $0, 9
	addi $a0, $0, 16 # 16 bytes, 4 bytes per element (length + 3 elements)
	syscall
	
	# pass local variables onto the stack (my_list, n)
	sw $v0, -4($fp) # store the address of the list on the stack
	# store n on the stack (assign n=3)
	addi $t0, $0, 3
	sw $t0, -8($fp)
	
	# assigning elements to the array
	lw $t0, -4($fp) # load the address of the array
	
	# store length of array
	addi $t1, $0, 3
	sw $t1, 0($t0) # store 3 at address of array
	
	# store first element of array
	addi $t1, $0, 2
	sw $t1, 4($t0) # store 2 at address of array
	
	# store second element of array
	addi $t1, $0, 4
	sw $t1, 8($t0) # store 4 at address of array
	
	# store third element of array
	addi $t1, $0, 6
	sw $t1, 12($t0) # store 6 at address of array
	
	# create space for arguments (list and n)
	addi $sp, $sp, -8
	
	lw $t0, -4($fp) # load address of list into $t0
	sw $t0, 0($sp) # store address on stack at 0($sp)
	
	lw $t0, -8($fp) # load n into $t0
	sw $t0, 4($sp) # store n on stack at 4($sp)
	
	# call function using jal get_multiples
	jal get_multiples
	
	# -------- after function call ----------------------
	
	# clear arguments off the stack
	addi $sp, $sp, 8
	
	# store return value in $t3
	addi $t3, $v0, 0 
	
	# print "The number of multiples of"
    addi $v0, $0, 4
    la $a0, final
    syscall

	# print "3" aka n
    addi $v0, $0, 1
    # n = t0
    lw $t0, -8($fp) # t0 = n
    addi $a0, $t0, 0 # accessing local variable n
    syscall

    # print "is"
    addi $v0, $0, 4
    la $a0, is
    syscall
    
    # print the number of multiples
    addi $v0, $0, 1
    add $a0, $0, $t3
    syscall
    
	# don't need to clear locals because it is main function
	addi $v0, $0, 10 # exit
	syscall
	
	
get_multiples:

	addi $sp, $sp, -8 # make space for $ra and $fp
	
	# save the value of $ra on the stack
	sw $ra, 4($sp)
	
	# save the value of $fp on the stack
	sw $fp, 0($sp)
	
	# copy $sp to $fp
	addi $fp, $sp, 0
	
	# allocate local variables on the stack (i and count)
	addi $sp, $sp, -8 # move the stack pointer up 8 bytes
	
	# initalise count and i to 0
	sw $0, -4($fp) # moving "count" onto the stack at -4($fp)
	sw $0, -8($fp) # moving i onto the stack at -8($fp)
	
	
loop:	# loop over array
	# determine whether to end loop
	lw $t0, -8($fp) # $t0 = i
	# just saved $ja and $ra to stack, so array size moved down 8 bytes from frame pointer
	
	lw $t2, 8($fp) # store array address in $t3
	lw $t1, ($t2) #load the value at the address $t3 into $t2
	
	slt $t2, $t0, $t1 # $t2 = 1 if i<size else 0
	beq $t2, $0, end # goto end if $t2 = 0 else continue

	# get list[i]
	lw $t0, -8($fp) # $t0 = i
	lw $t1, 8($fp) # $t1 = list[-1] address (len)
	sll $t0, $t0, 2 # i*=4
	add $t2, $t0, $t1 # $t2 = list[i-1]
	
	lw $t0, 4($t2) # load list[i] into $t0
	
	# check if list[i] % n == 0
	lw $t1, 12($fp) # $t1 = n
	div $t0, $t1
	mfhi $t2
	bne $t2, $0, i_add # if list[i] % n != 0, branch to increment i
	
	# check if list[i] == n
	lw $t1, 4($fp) # $t1 = n
	beq $t0, $t1, i_add # if list[i] == n, branch to increment i
	
	# if code reaches this stage, list[i] % n == 0 and list[i] != n
	# increment count
	lw $t0, -4($fp) # $t0 = count
	addi $t0, $t0, 1 # $t0 += 1
	sw $t0, -4($fp)

i_add:	lw $t0, -8($fp) # increment i
	addi $t0, $t0, 1
	sw $t0, -8($fp)

	j loop	# loop

end:	
	# set $v0 as the return value
	lw $v0, -4($fp) # sets the return value to count
	
	# clear parameters off the stack
	addi $sp, $sp, 8
	
	# restore saved $fp off stack
	lw $fp, 0($sp) # restore $fp
	
	# restore $ra off stack
	lw $ra, 4($sp) # restore $ra
	
	# deallocate space for $ra and $fp
	addi $sp, $sp, 8
	
	# returns to caller by jumping to $ra
	jr $ra