#!/usr/bin/env python3

from math import sqrt
import doctest
from copy import deepcopy
from random import shuffle, randint

small = [[1, 0, 0, 0],
         [0, 4, 1, 0],
         [0, 0, 0, 3],
         [4, 0, 0, 0]]

small2 = [[0, 0, 1, 0],
          [4, 0, 0, 0],
          [0, 0, 0, 2],
          [0, 3, 0, 0]]

big = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 7, 8, 9, 0, 0, 0],
       [7, 8, 0, 0, 0, 0, 0, 5, 6],
       [0, 2, 0, 3, 6, 0, 8, 0, 0],
       [0, 0, 5, 0, 0, 7, 0, 1, 0],
       [8, 0, 0, 2, 0, 0, 0, 0, 5],
       [0, 0, 1, 6, 4, 0, 9, 7, 0],
       [0, 0, 0, 9, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 3, 0, 0, 0, 2]]

big2 = [[7, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 5, 0, 0, 0, 9, 0, 0, 0],
        [8, 0, 0, 0, 3, 0, 0, 4, 0],
        [0, 0, 0, 7, 6, 0, 0, 0, 8],
        [6, 2, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 7, 0],
        [0, 0, 0, 6, 0, 0, 9, 8, 0],
        [0, 0, 0, 0, 2, 7, 3, 0, 0],
        [0, 0, 2, 0, 8, 0, 0, 5, 0]]

big3 = [[0, 0, 8, 1, 9, 0, 0, 0, 6],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 6, 0, 0, 1, 3, 0],
        [0, 0, 6, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 2, 0, 0, 5],
        [0, 0, 0, 0, 3, 0, 9, 0, 0],
        [0, 1, 0, 4, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 5, 7]]

big4 = [[0, 0, 0, 6, 0, 0, 2, 0, 0],
        [8, 0, 4, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 0, 0, 0],
        [4, 0, 5, 0, 0, 0, 0, 0, 7],
        [7, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 5, 0, 0, 0, 8],
        [3, 0, 0, 0, 7, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 1, 9, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 6, 0]]

giant = [[0,  0, 13,  0,  0,  0,  0,  0,  2,  0,  8,  0,  0,  0, 12, 15],
         [7,  8, 12,  2, 10,  0,  0, 13,  0,  0, 14, 11,  6,  9,  0,  4],
         [11, 10,  0,  0,  0,  6, 12,  5,  0,  3,  0,  0,  0, 14,  0,  8],
         [1,  0,  0,  0, 14,  0,  2,  0,  0,  4,  6,  0, 16,  3,  0, 13],
         [12,  6,  0,  3,  0,  0, 16, 11,  0, 10,  1,  7, 13, 15,  0,  0],
         [0, 13,  0,  0,  0, 15,  8,  0, 14,  0,  0,  0,  0, 16,  5, 11],
         [8,  0, 11,  9, 13,  0,  7,  0,  0,  0,  0,  3,  2,  4,  0, 12],
         [5,  0,  0, 16, 12,  9,  0, 10, 11,  2, 13,  0,  0,  0,  8,  0],
         [0,  0,  0,  0, 16,  8,  9, 12,  0,  0,  0,  0,  0,  6,  3,  0],
         [2, 16,  0,  0,  0, 11,  0,  0,  7,  0, 12,  6,  0, 13, 15,  0],
         [0,  0,  4,  0,  0, 13,  0,  7,  3, 15,  0,  5,  0,  0,  0,  0],
         [0,  7,  0, 13,  4,  5, 10,  0,  1,  0, 11, 16,  9,  0, 14,  2],
         [0,  2,  8,  0,  9,  0,  0,  0,  4,  0,  7,  0,  0,  5,  0,  0],
         [14,  0,  0,  0, 15,  2, 11,  4,  9, 13,  3,  0, 12,  0,  0,  0],
         [0,  1,  9,  7,  0,  0,  5,  0,  0, 11, 15, 12,  0,  0,  0,  0],
         [16,  3, 15,  0,  0, 14, 13,  6, 10,  1,  0,  2,  0,  8,  4,  9]]

giant2 = [[0,  5,  0,  0,  0,  4,  0,  8,  0,  6,  0,  0,  0,  0,  9, 16],
          [1,  0,  0,  0,  0,  0,  0, 13,  4,  0,  0,  7, 15,  0,  8,  0],
          [13,  0,  0,  0,  0,  7,  3,  0,  0,  0,  0,  9,  5, 10,  0,  0],
          [0, 11, 12, 15, 10,  0,  0,  0,  0,  0,  5,  0,  3,  4,  0, 13],
          [15,  0,  1,  3,  0,  0,  7,  2,  0,  0,  0,  0,  0,  5,  0,  0],
          [0,  0,  0, 12,  0,  3,  0,  5,  0, 11,  0, 14,  0,  0,  0,  9],
          [4,  7,  0,  0,  0,  0,  0,  0, 12,  0, 15, 16,  0,  0,  0,  0],
          [0,  0,  0,  0, 14,  0, 15,  0,  6,  9,  0,  0,  0,  0, 12,  0],
          [3,  0, 15,  4,  0, 13, 14,  0,  0,  0,  0,  1,  0,  0,  7,  8],
          [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9, 10,  0,  0,  0,  0],
          [11,  0, 16, 10,  0,  0,  0,  0,  0,  7,  0,  0,  0,  3,  5,  0],
          [0,  0, 13,  0,  0,  0,  0,  0, 14,  0, 16, 15,  0,  9,  0,  1],
          [9,  0,  2,  0,  0, 14,  0,  4,  8,  0,  0,  0,  0,  0,  0,  0],
          [0, 14,  0,  0,  0,  0,  0, 10,  9,  0,  3,  0,  0,  0,  1,  7],
          [8,  0,  0,  0, 16,  0,  0,  1,  2, 14, 11,  4,  0,  0,  0,  3],
          [0,  0,  0,  1,  0,  0,  5,  0,  0, 16,  0,  6,  0, 12,  0,  0]]

giant3 = [[0,  4,  0,  0,  0,  0,  0, 12,  0,  1,  0,  0,  9,  0,  8,  0],
          [15, 14,  0,  0,  9,  0,  0, 13,  8,  0,  0, 10,  1,  0,  0,  0],
          [0,  7,  0,  0,  0,  0,  0,  8, 16,  0, 14,  0,  0,  2,  0,  0],
          [0,  0,  0,  9,  0,  0, 11,  0,  0,  0,  0,  0,  5,  0,  0, 15],
          [3,  0, 12,  0,  7,  0, 10,  0,  0, 11,  2,  0,  0,  0,  0,  6],
          [14,  8,  0,  0,  0, 12,  0,  6,  0,  0,  0, 16,  0,  0,  0, 10],
          [0, 16,  0,  0, 13,  0,  0,  0,  0,  0,  0,  0,  0,  0, 12,  0],
          [6,  0,  0,  0,  0,  8,  0,  5,  1,  7, 13,  0, 11,  0,  0, 14],
          [0,  0,  0,  2,  0,  0, 16,  0, 15, 12,  0,  3, 10,  7,  0,  0],
          [0,  9,  0,  5, 11,  0,  3,  0,  4, 13, 16,  0,  0, 15,  6,  0],
          [0,  0,  0,  0,  5,  4,  0,  0,  9,  6,  0,  2,  0,  0,  0,  0],
          [1,  0,  0,  0,  0, 15, 12,  0,  0,  0,  5,  0,  0,  0,  9,  0],
          [12, 10,  0, 15,  0,  1,  0,  0,  2,  9,  3,  4,  0,  0,  5,  0],
          [0,  0,  0,  3, 10,  0,  4,  0,  0, 15,  0,  0,  0,  0,  0,  0],
          [0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10, 11],
          [11,  6,  8,  0,  0,  0, 15,  0, 14,  0,  0,  0,  0, 13,  0,  2]]

sudokus = [[], [], [small, small2], [
    big, big2, big3, big4], [giant, giant2, giant3]]


def print_board(board):
    size = len(board)
    k = int(size**(1/2))  # grid size
    spacerLen = size + k + 1  # length of the horizontal spacers between grids
    charA = 65  # for the letter when n>=10

    output = '-' * spacerLen + '\n'  # create top horizontal line

    for i in range(1, size + 1):
        row = '|'  # each row starts
        for j in range(1, size + 1):  # iterate over each row
            num = board[i - 1][j - 1]
            if type(num) == type(''):
                row += num  # if the element is the * for hints
            else:
                char = chr(charA + num - 10)  # if num >= 10 use char
                row += char if num >= 10 else ' ' if num == 0 else str(num)
            if j % k == 0:
                row += '|'  # if we are at the end of the grid add the end '|'
        output += row + '\n'  # add the row to the overall output
        if i % k == 0:  # if we are at the end of the grid vertically, add the spacer
            output += '-' * spacerLen
            if i != size:
                output += '\n'  # add a new line at the end of each spacer except for the last one
    print(output)


def subgrid_values(board, r, c):
    n = len(board)
    k = int(n**(1/2))
    res = []
    for i in range((r // k) * k, ((r // k) + 1) * k):
        for j in range((c // k) * k, ((c // k) + 1) * k):
            if board[i][j]:
                res.append(board[i][j])
    return res


def options(board, r, c):
    if board[r][c]:
        return []

    res = []
    n = len(board)
    col_vals = [board[s][c] for s in range(n)]
    row_vals = board[r]
    subgrid_vals = subgrid_values(board, r, c)
    for x in range(1, n+1):
        if x not in col_vals and x not in row_vals and x not in subgrid_vals:
            res.append(x)
    return res


def hint(board):
    # initialise the lowest value for the amount of options
    lowestValue = len(board)
    lowestIndexes = {}  # initialise the indexes of the lowest options
    for i in range(len(board)):  # iterating over each element of the board
        for j in range(len(board[i])):
            if board[i][j] == 0:  # if the board element is currently not solved
                opt = options(board, i, j)
                num = len(opt)  # find how many options
                if num == 1:  # if there's one option we can finish this early as this is best case
                    return {'i': i, 'j': j, 'o': opt}
                elif num < lowestValue:  # otherwise add to the lowest value if necessary
                    lowestValue = num
                    lowestIndexes = {'i': i, 'j': j, 'o': opt}
    return lowestIndexes


def play(board):
    # initialise the start board as a copy of the actual board, used to restart game
    start = deepcopy(board)
    # initialise previous moves, this is to use the undo functionality
    lastMove = {'i': [], 'j': []}
    print_board(board)
    while True:
        # test to see if the length of elements that are 0 or * in the board is 0, if it is zero board is solved
        if solved(board):
            print('Sodoku Complete!')
            return
        inp = input().split(' ')
        if len(inp) == 3 and inp[0].isdecimal() and inp[1].isdecimal() and inp[2].isdecimal():
            i = int(inp[0])
            j = int(inp[1])
            x = int(inp[2])
            # check to see if number inputted is valid
            option = options(board, i, j)
            if x in option and board[i][j] == 0:
                # add move to last move in order to be able to undo it
                lastMove['i'].append(i)
                lastMove['j'].append(j)
                board[i][j] = x
            else:
                # error message
                print('Invalid Number')
            print_board(board)
        elif len(inp) == 3 and (inp[0] == 'n' or inp[0] == 'new') and inp[1].isdecimal() and inp[2].isdecimal():
            k = int(inp[1])
            d = int(inp[2])
            if k < len(sudokus) and 0 < d <= len(sudokus[k]):
                board = sudokus[k][d-1]
                # reinitialise the start board
                start = deepcopy(board)
                print_board(board)
            else:
                print('board not found')
        elif inp[0] == 'r' or inp[0] == 'restart':
            # restarting redefines the board as a copy of the start board
            board = deepcopy(start)
            print_board(board)
        elif inp[0] == 'u' or inp[0] == 'undo':
            # can only undo if moves > 1
            if len(lastMove['i']) > 0 and len(lastMove['j']) > 0:
                last_i = lastMove['i'][-1]
                last_j = lastMove['j'][-1]
                # change the last element changed back to 0
                board[last_i][last_j] = 0
                lastMove['i'].pop()
                lastMove['j'].pop()  # remove the last elements from lastMove
            else:
                print("no more moves to undo")  # error statement
            print_board(board)
        elif inp[0] == 'h' or inp[0] == 'hint':
            indexes = hint(board)  # retrieve hint from function
            # change the element to a star to highlight it
            board[indexes['i']][indexes['j']] = '*'
            print_board(board)
            # print the board along with the index of the hinted element
            print('({}, {})'.format(indexes['i'], indexes['j']))
        elif inp[0] == 'i' or inp[0] == 'infer':
            board = inferred(board)  # board is updated
            print_board(board)  # board is printed
        elif inp[0] == 's' or inp[0] == 'solve':
            board = backtracking(board)[0]  # board is solved
            print_board(board)  # board is printed
            print('Sodoku Complete!')  # complete message is printed
            return
        elif len(inp) == 2 and (inp[0] == 'g' or inp[0] == 'generate') and inp[1].isdecimal():
            k = int(inp[1])
            if k < 1 or k > 4 or k % 1 != 0:  # make sure k is valid
                print('Invalid size of board')
            else:
                # generate, print and update the starting board
                board = generate(k)
                start = deepcopy(board)
                print_board(board)
        elif inp[0] == 'q' or inp[0] == 'quit':
            return
        else:
            print('Invalid Input')


def value_by_single(board, i, j):
    n = len(board)
    k = round(sqrt(n))

    forwardOptions = options(board, i, j)  # get options from function
    if len(forwardOptions) == 1:  # if there is only one option, return that value
        return forwardOptions[0]

    # three empty sets are defined for row, col and subgrid opts
    row_opts, col_opts, sub_opts = set(), set(), set()

    for x in range(n):  # adding all valid options to respective sets
        if x != j and not board[i][x]:
            for o in options(board, i, x):
                row_opts.add(o)
        if x != i and not board[x][j]:
            for o in options(board, x, j):
                col_opts.add(o)
        r = (i // k) * k + x // k
        c = (j // k) * k + x % k
        if (r != i or c != j) and not board[r][c]:
            for o in options(board, r, c):
                sub_opts.add(o)

    all_opts = [row_opts, col_opts, sub_opts]
    for x in forwardOptions:  # iterating over the sets
        for y in all_opts:
            if x not in y:  # if a forward option is not in that set, return that option
                return x

    return None


def inferred(board):
    size = len(board)
    newBoard = deepcopy(board)
    tested = 0  # initilising the tested variable, this will store how many places on the board have no options
    # while the amount of places that have no options doesnt equal the amount of places we loop
    while tested < size**2:
        tested = 0
        # we loop through each position
        for i in range(size):
            for j in range(size):
                # if the spot is filled we add to tested and move on
                if newBoard[i][j]:
                    tested += 1
                    continue
                # otherwise we check the value using our function
                value = value_by_single(newBoard, i, j)
                # if the value is none, we increase tested, otherwise the board is updated
                if value:
                    newBoard[i][j] = value
                else:
                    tested += 1
        # this continues until either the board is full or there are no moves left in the board using the singles
    return newBoard


def solved(board):
    # returns true if the amount of zeroes in the board is zero
    size = len(board)
    return len([board[i][j] for i in range(size) for j in range(size) if board[i][j] == 0]) == 0


def estimated_time(board):
    from time import time
    start = time()
    inferred(small)
    total = time()-start  # first time inferred on the smallest board
    mine = 0.0007  # this is the average on my laptop
    # find a ratio of these two times (add 0.2 to account for errors)
    ratio = total / mine + 0.2
    sudokus_test = [small, small2, big, big2,
                    big3, big4, giant, giant2, giant3]
    sudokus_time = [0.00025, 0.00017, 0.0085,
                    0.01, 0.155, 7.5, 0.019, 0.57, 53]  # this is the averages of all of my times for each board
    time_estimate = 0
    for x in range(len(sudokus_test)):
        if sudokus_test[x] == board:  # find which board is inputted
            # redefine the time variable
            time_estimate = ratio * sudokus_time[x]
            break
    # return an informative time estimate
    return 'Less than a second' if time_estimate < 1 else 'about {}s'.format(round(time_estimate))


def backtracking(board, normal=True, part=[]):
    if part == []:  # since part starts empty we need to update it to the inferred state of the board
        if normal:  # this normal variable is used to decipher between when backtracking is used alone vs when it is used by the generate function
            print('\nSolving... estimated time = {}\n'.format(
                estimated_time(board)))
        return backtracking(board, normal, inferred(board))

    elif solved(part):  # using the solved function to test whether part is solved
        return [part]

    else:
        res = []
        pos = hint(part)  # choosing the easiest position first
        for o in pos['o']:
            aug_p = inferred(part)  # inferring the part
            if aug_p[pos['i']][pos['j']] == 0:  # if the inference hasn't worked
                # replace with one of the options
                aug_p[pos['i']][pos['j']] = o
            res += backtracking(board, normal, aug_p)  # call recursively
        return res


def generate(k):
    def grid_row_swap(sudoku):
        new = []
        for x in range(k):
            row = []
            for y in range(k):
                row += sudoku[x*k+y]
            new.append(row)
        shuffle(new)
        res = []
        for x in range(len(sudoku)):
            row = []
            for y in range(len(sudoku)):
                i = (x*len(sudoku)+y) // k**3
                j = (x*len(sudoku)+y) % k**3
                row.append(new[i][j])
            res.append(row)
        return res

    def grid_col_swap(sudoku): 
        new = []
        for x in range(k):
            set_ = []
            for y in range(len(sudoku)):
                sub_row = []
                for z in range(k):
                    i = y
                    j = x*k + z
                    sub_row.append(sudoku[i][j])
                set_.append(sub_row)
            new.append(set_)
        shuffle(new)
        res = []
        for x in range(len(sudoku)):
            row = []
            for y in range(k):
                i = y
                j = x
                row += new[i][j]
            res.append(row)
        return res

    def row_swap(sudoku):  
        new = []
        for x in range(0, k**2, k):
            part = sudoku[x:x+k]
            shuffle(part)
            new += part
        return new

    def col_swap(sudoku): 
        transpose = [[sudoku[j][i]
                      for j in range(len(sudoku))] for i in range(len(sudoku))]
        res = []
        for x in range(0, k**2, k):
            part = transpose[x:x+k]
            shuffle(part)
            res += part
        res = [[res[j][i] for j in range(len(res))] for i in range(len(res))]
        return res

    def number_swap(sudoku):  
        new = [[sudoku[i][j]
                for j in range(len(sudoku))] for i in range(len(sudoku))]
        initials = [i+1 for i in range(len(sudoku))]
        swaps = [i+1 for i in range(len(sudoku))]
        shuffle(initials)
        shuffle(swaps)
        for i in range(len(initials)):
            for x in range(len(sudoku)):
                for y in range(len(sudoku)):
                    if new[x][y] == initials[i]:
                        new[x][y] = swaps[i]
                    elif new[x][y] == swaps[i]:
                        new[x][y] = initials[i]
        return new

    print('\nGenerating .... ')  # for viewer usage
    sudoku = backtracking(sudokus[k][1], False)[
        0]  # solve a given board of size k
    transformations = [grid_col_swap, grid_row_swap,
                       row_swap, col_swap, number_swap]
    shuffle(transformations)
    for x in transformations:
        sudoku = x(sudoku)  # transform the sudoku

    full_spots = [[i, j] for i in range(len(sudoku))
                  for j in range(len(sudoku)) if sudoku[i][j]]  # get all spots on the board in [i,j] form
    shuffle(full_spots)  # shuffle all the spots so they are in random order

    last_move = {'i': 0, 'j': 0, 'n': 0}  # initialise the last move
    for x in range(len(full_spots)):  # makes sure to check all spots on the board
        i, j = full_spots[x]  # define i and j from full_spots
        # save the last move
        last_move['i'], last_move['j'], last_move['n'] = i, j, sudoku[i][j]
        sudoku[i][j] = 0  # reset the spot to 0
        # if the number of solutions is not 1, undo the last move
        if len(backtracking(sudoku, False)) != 1:
            sudoku[last_move['i']][last_move['j']] = last_move['n']
        # shows completion percentage
        print('{}%'.format(round((x+1)/(len(full_spots))*100, 2)))
    print('Done!\n')
    return sudoku


play(big)