#!/usr/bin/env python3
from math import sqrt, pi, ceil
from sys import float_info
from random import shuffle 
from timeit import default_timer as timer  


def merge(lst1, lst2):
    sorted_merge = []
    i = 0
    j = 0
    while i < len(lst1) and j < len(lst2):
        if lst1[i] < lst2[j]:
            sorted_merge.append(lst1[i])
            i += 1
        else:
            sorted_merge.append(lst2[j])
            j += 1
    return sorted_merge + lst1[i::] + lst2[j::]


def merge_sort(lst):
    merged = []
    for x in range(0, len(lst), 2):
        if x+1 == len(lst):
            merged.append([lst[x]])
        else:
            merged.append(merge([lst[x]], [lst[x+1]]))

    while len(merged[0]) < len(lst):
        ran = ceil(len(merged)/2)
        for x in range(ran):
            if x+1 == len(merged):
                continue
            merged[x:x+2] = [merge(merged[x], merged[x+1])]
    return merged[0]


def selection_sort(lst):
    i = 0
    while i < len(lst)-1:
        swapIndex = lst[i:].index((min(lst[i:]))) + i
        lst[i], lst[swapIndex] = lst[swapIndex], lst[i]
        i += 1


def insertion_sort(lst):
    for j in range(len(lst)):
        while j > 0 and lst[j - 1] > lst[j]:
            lst[j - 1], lst[j] = lst[j], lst[j - 1]
            j -= 1


def sort_analysis(func, n):
    non_dec = [i for i in range(1, n+1)]
    dec = [i for i in range(n, 0, -1)]
    random = [i for i in range(1, n+1)]
    shuffle(random)

    start = timer()
    func(non_dec)
    end = timer()
    non_dec_time = end - start

    start = timer()
    func(dec)
    end = timer()
    dec_time = end - start

    start = timer()
    func(random)
    end = timer()
    random_time = end - start

    return {"non-decreasing": non_dec_time, "decreasing": dec_time, "random": random_time}