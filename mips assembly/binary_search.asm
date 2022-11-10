# Title: 	Binary search algorithm.
# Author: 	Samir Gupta
# Date: 	18/03/2022

	.text

	.globl main
	.globl binary_search

main: 	
	# length = -4($fp)
	# array address = -8($fp)
	# index = -12($fp)
	
	# copy sp into fp
	addi $fp, $sp, 0
	
	# allocate 8 bytes for length of array and array address
	addi $sp, $sp, -8
	
	addi $t0, $0, 5
	sw $t0, -4($fp) # len = 5
	
	# allocate space for array
	addi $v0, $0, 9 
	lw $t0, -4($fp)
	sll $t0, $t0, 2
	addi $a0, $t0, 4 
	syscall
	sw $v0, -8($fp) # address = array address
	sw $t0, ($v0)
	
	# store array values
	lw $t0, -8($fp)
	addi $t1, $0, 1
	sw $t1, 4($t0) # arr[0] = 1
	addi $t1, $0, 20
	sw $t1, 8($t0) # arr[1] = 20
	addi $t1, $0, 30
	sw $t1, 12($t0) # arr[2] = 30
	addi $t1, $0, 31
	sw $t1, 16($t0) # arr[3] = 31
	addi $t1, $0, 35
	sw $t1, 20($t0) # arr[4] = 35
	
	# allocate 4 bytes for each argument (array, target, low, high)
	addi $sp, $sp, -16
	
	# store address as arg1
	lw $t0, -8($fp) 
	sw $t0, 0($sp)
	
	 # store target as arg2
	addi $t0, $0, 1
	sw $t0, 4($sp)
	
	 # store 0 for arg3 (low)
	addi $t0, $0, 0
	sw $t0, 8($sp)
	
	# store len-1 for arg4 (high)
	lw $t0, -4($fp) 
	addi $t0, $t0, -1
	sw $t0, 12($sp)
	
	# run binary search
	jal binary_search
	
	# clear 4 arguments
	addi $sp, $sp, 16
	
	# allocate 4 bytes for index variable
	addi $sp, $sp, -4
	
	# store index variable
	sw $v0, -12($fp)
	
	# print index
	lw $a0, -12($fp)
	addi $v0, $0, 1
	syscall
	
	# clear locals and exit
	addi $sp, $sp, 12
	addi $v0, $0, 10
	syscall
	
binary_search: 
	# address = 8($fp)
	# target = 12($fp)
	# low = 16($fp)
	# high = 20($fp)
	# mid = -4($fp)
	
	addi $sp, $sp, -8 # alloc space
	sw $ra, 4($sp) # save $ra
	sw $fp, 0($sp) # save $fp
	addi $fp, $sp, 0 # copy $sp $fp
	
	lw $t0, 16($fp)
	lw $t1, 20($fp)
	slt $t2, $t1, $t0 # is high < low?
	bne $t2, $0, not_found # if high < low branch to not found
	
	# allocate for local variable mid
	addi $sp, $sp, -4
	
	# calculate and store mid
	lw $t0, 16($fp)
	lw $t1, 20($fp)
	add $t0, $t1, $t0
	srl $t0, $t0, 1
	sw $t0, -4($fp)
	
	# if list[mid] == target
	lw $t0, 8($fp)
	lw $t1, 12($fp)
	lw $t2, -4($fp)
	sll $t2, $t2, 2
	add $t0, $t0, $t2
	lw $t3, 4($t0) # $t3 = list[mid]
	beq $t3, $t1, equal # if list[mid] == target, branch to equal
	
	# if list[mid] > target
	lw $t0, 8($fp)
	lw $t1, 12($fp)
	lw $t2, -4($fp)
	sll $t2, $t2, 2
	add $t0, $t0, $t2
	lw $t3, 4($t0) # $t3 = list[mid]
	slt $t0, $t1, $t3 # is target < list[mid] ?
	bne $t0, $0, bigger # branch to bigger if target < list[mid]
	
	# else we go to smaller
	
smaller: 
	# allocate 4 arguments
	addi $sp, $sp, -16
	
	# arg1 = address
	lw $t0, 8($fp)
	sw $t0, 0($sp)
	
	# arg2 = target
	lw $t0, 12($fp)
	sw $t0, 4($sp)
	
	# arg3 = mid+1
	lw $t0, -4($fp)
	addi $t0, $t0, 1
	sw $t0, 8($sp)
	
	# arg4 = high
	lw $t0, 20($fp)
	sw $t0, 12($sp)
	
	# recursive call
	jal binary_search
	
	# deallocate arguments and local variable
	addi $sp, $sp, 20
	
	# return result (already stored in $v0)
	lw $fp, 0($sp)
	lw $ra, 4($sp)
	addi $sp, $sp, 8
	jr $ra
	
bigger: 
	# allocate 4 arguments
	addi $sp, $sp, -16
	
	# arg1 = address
	lw $t0, 8($fp)
	sw $t0, 0($sp)
	
	# arg2 = target
	lw $t0, 12($fp)
	sw $t0, 4($sp)
	
	# arg3 = low
	lw $t0, 16($fp)
	sw $t0, 8($sp)
	
	# arg4 = mid-1
	lw $t0, -4($fp)
	addi $t0, $t0, -1
	sw $t0, 12($sp)
	
	# recursive call
	jal binary_search
	
	# deallocate arguments and local variable
	addi $sp, $sp, 20
	
	# return result (already stored in $v0)
	lw $fp, 0($sp)
	lw $ra, 4($sp)
	addi $sp, $sp, 8
	jr $ra

equal:
	# return mid
	lw $t0, -4($fp)
	addi $sp, $sp, 4
	addi $v0, $t0, 0
	lw $fp, 0($sp)
	lw $ra, 4($sp)
	addi $sp, $sp, 8
	jr $ra
	
not_found:
	# return -1
	addi $v0, $0, -1
	lw $fp, 0($sp)
	lw $ra, 4($sp)
	addi $sp, $sp, 8
	jr $ra