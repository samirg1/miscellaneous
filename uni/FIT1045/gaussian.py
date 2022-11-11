#!/usr/bin/env python3
from copy import deepcopy
def gaussian_elim(a, b):
    from copy import deepcopy
    def pivot_index(u, j):
        for x in range(j, len(u)):
            if u[x][j]:
                return x

    def triangular(a, b):
        u, c = deepcopy(a), deepcopy(b)
        n = len(u)
        for j in range(n):
            k = pivot_index(u, j)
            u[j], u[k] = u[k], u[j]
            c[j], c[k] = c[k], c[j]
            for i in range(j + 1, len(a)):
                q = u[i][j] / u[j][j]
                u[i] = [u[i][l] - q*u[j][l] for l in range(n)]
                c[i] = c[i] - q*c[j]
        return u, c

    def solve_backsub(u, b):
        n = len(b)
        x = n*[0]
        for i in range(n-1, -1, -1):
            s = sum(x[j] * u[i][j] for j in range(n-1, i, -1))
            x[i] = (b[i] - s)/u[i][i]
        return x

    def solve_gauss_elim(a, b):
        u, c = triangular(a, b)
        return solve_backsub(u, c)

    return solve_gauss_elim(a, b)


def is_upper_triangular(a):
    for x in range(len(a)):
        for y in range(x):
            if a[x][y]:
                return False
    return True


def is_row_echelon(a):
    if not is_upper_triangular(a):
        return False

    for x in range(len(a)):
        if not a[x][x]:
            for y in range(x+1, len(a)):
                if a[y][y]:
                    return False
            break
    return True


def pivot_index(a, j, p=None):
    for x in range(j, len(a)):
        if a[x][j]:
            return x
    return None


def echelon(a, b):
    u, c = deepcopy(a), deepcopy(b)
    n = len(u)
    for i in range(n):
        k = 0
        i2 = i
        for j in range(n):
            k = pivot_index(u, j)
            if k:
                i2 = j
                break
        u[i], u[k] = u[k], u[i]
        c[i], c[k] = c[k], c[i]
        for z in range(i + 1, len(a)):
            q = u[z][i2] / u[i][i2]
            u[z] = [u[z][l] - q*u[i][l] for l in range(n)]
            c[z] = c[z] - q*c[i]
    return (u, c)


def solve_by_back_substitution(u, b):
    n = len(b)
    x = n*[float(0)]
    for i in range(n-1, -1, -1):
        change = False
        for j in range(n):
            if u[i][j]:
                s = sum(x[k] * u[i][k] for k in range(n-1, j, -1))
                x[j] = (b[i]-s)/u[i][j]
                change = True
                break
        if not change:  # if nothing has happened i.e. row of zeroes
            if b[i] != 0:  # check if the b value of the ith row is zero
                return None  # if not, there is no solutions
    return x