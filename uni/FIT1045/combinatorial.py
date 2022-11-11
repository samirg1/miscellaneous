#!/usr/bin/env python3
def lex_less_eq(a, b):
    for i in range(len(a)):
        if a[i] > b[i]:
            return False
        elif a[i] < b[i]:
            return True
    return True


def rbitlists(n, part=[]):
    if len(part) == n:
        return [part]
    else:
        res = []
        opts = [0, 1]
        for o in opts:
            aug = part+[o]
            res += rbitlists(n, aug)
        return res


def rpermutations(lst, part=[]):
    if len(part) == len(lst):
        return [part]
    else:
        res = []
        opts = [lst[i] for i in range(len(lst)) if not lst[i] in part]
        for o in opts:
            aug = part + [o]
            res += rpermutations(lst, aug)
        return res


def bounded_lists(upper_bounds, part=[]):
    if len(part) == len(upper_bounds):
        return [part]
    else:
        res = []
        opts = range(0, upper_bounds[len(part)] + 1)
        for o in opts:
            aug = part + [o]
            res += bounded_lists(upper_bounds, aug)
        return res


def greedy_exchange(amount, denominations):
    tot = 0
    denoms = [0]*len(denominations)
    while tot != amount:
        for x in range(len(denominations)):
            if tot + denominations[x] <= amount:
                tot += denominations[x]
                denoms[x] += 1
                break
    return denoms


def brute_force_coin_exchange(amount, denoms):
    def valid(lst):
        tot = 0
        for i in range(len(denoms)):
            tot += denoms[i]*lst[i]
        return tot == amount

    upper_bounds = [amount // denoms[i] for i in range(len(denoms))]
    possibles = bounded_lists(upper_bounds)
    valids = filter(valid, possibles)
    return min(valids, key=sum)


def backtracking_exchange(amount, denoms, part=[], tot=0, best=[], best_n=0, part_n=0):
    def options(tot, best_n, part_n):
        return [] if part_n >= best_n else [x for x in range(len(denoms)) if denoms[x] + tot <= amount]

    def completed(tot):
        return tot == amount

    if part == []:
        return backtracking_exchange(amount, denoms, [0]*len(denoms), tot, [amount//denoms[-1]], amount//denoms[-1], part_n)

    elif completed(tot):
        return part

    for o in options(tot, best_n, part_n):
        aug_p = part + []
        aug_p[o] += 1
        aug_p_n = part_n + 1
        aug_t = tot + denoms[o]
        sol = backtracking_exchange(amount, denoms, aug_p, aug_t, best, best_n, aug_p_n)
        best, best_n = sol, sum(sol)
    return best


def palindrome_binary(n, part=[]):
    def palindrome(lst):
        for x in range(len(lst)//2):
            if lst[x] != lst[-(x+1)]:
                return False
        return True
    if len(part) == n:
        return [part] if palindrome(part) else []
    else:
        res = []
        for o in [0, 1]:
            aug = part + [o]
            res += palindrome_binary(n, aug)
        return res


def all_paths(M, u, v, part=[]):
    def options(M, part):
        opts = []
        for x in range(len(M)):
            if M[part[-1]][x] and not x in part:
                opts.append(x)
        return opts

    if part == []:
        return all_paths(M, u, v, [u])

    elif part[-1] == v:
        return [part]
    else:
        res = []
        for o in options(M, part):
            aug = part + [o]
            res += all_paths(M, u, v, aug)
        return res