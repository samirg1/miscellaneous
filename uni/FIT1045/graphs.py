#!/usr/bin/env python3
from copy import deepcopy
from random import shuffle, randint
import sample_graphs
from sample_graphs import neighbours, print_grid_traversal
from collections import deque

def degree(graph, vertex):
    return graph[vertex].count(True)


def is_path(graph, path):
    for x in path:
        count = path.count(x)
        if count > 2 or (count > 1 and not (path[0] == x and path[-1] == x)):
            return False
    for x in range(len(path)-1):
        if graph[path[x]][path[x+1]] != 1:
            return False
    return True


def print_as_grid(graph, n):
    def index(r, c):
        return r*n + c

    m = len(graph) // n

    for i in range(m):
        for j in range(n):
            print('*', end='')
            k = index(i, j)
            if j < n-1 and graph[k][index(i, j+1)]:
                print('---', end='')
            else:
                print('   ', end='')
        print('\n', end='')
        if i < m - 1:
            for j in range(n):
                k = index(i, j)
                if graph[k][index(i + 1, j)]:
                    print('|', end='')
                else:
                    print(' ', end='')
                if j < n-1:
                    print('   ', end='')
            print('\n', end='')


def grid_graph(m, n):
    vertices = m*n
    grid = [([0]*vertices).copy() for i in range(vertices)]

    # adding horizontal connections to upper triangle
    i = 1
    j = 0
    while i < vertices and j < vertices:
        if i % n != 0 and j-(n-1) % n != 0:
            grid[j][i] = 1
        i += 1
        j += 1

    # adding vertical connections to upper triangle
    i = n
    j = 0
    while i < vertices and j < vertices:
        grid[j][i] = 1
        i += 1
        j += 1

    # reflecting upper triangle to lower triangle as grid is symmetric
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 1 and grid[y][x] != 1:
                grid[y][x] = 1

    return grid


def spanning_tree(graph):
    vertices = len(graph)
    tree = [([0]*vertices).copy() for i in range(vertices)]
    conn = [0]
    while len(conn) < vertices:
        shuffle(conn)
        for i in conn:
            for j in range(vertices):
                if j not in conn and graph[i][j] == 1:
                    tree[i][j], tree[j][i], found = 1, 1, True
                    conn.append(j)
                    break
            if found:
                found = False
                break
    return tree


def sort_table(table, col):
    for j in range(len(table)):
        while j > 0 and table[j - 1][col] > table[j][col]:
            table[j - 1], table[j] = table[j], table[j - 1]
            j -= 1


def bfs_traversal(graph, s, goals=[]):
    visited = []
    boundary = deque([s])
    while len(boundary) > 0:
        v = boundary.popleft()
        visited += [v]
        if v in goals:
            return visited
        for w in neighbours(v, graph):
            if w not in visited and w not in boundary:
                boundary.append(w)
    return visited


def dfs_traversal(graph, s, goals=[]):
    visited = []
    boundary = [s]
    while len(boundary) > 0:
        v = boundary.pop()
        visited += [v]
        if v in goals:
            return visited
        for w in neighbours(v, graph):
            if w not in visited and w not in boundary:
                boundary.append(w)
    return visited


def bfs_path(graph, s, goals=[]):
    visited = []
    boundary = deque([s])
    parents = [None] * len(graph)
    vertex = None
    while len(boundary) > 0:
        v = boundary.popleft()
        visited += [v]
        for w in neighbours(v, graph):
            if w not in visited and w not in boundary:
                boundary.append(w)
                parents[w] = v
        if v in goals:
            vertex = v
            break
    path = deque([])
    path.append(vertex)
    while vertex != 0:
        path.appendleft(parents[vertex])
        vertex = parents[vertex]
    return path


def dfs_path(graph, s, goals=[]):
    visited = []
    boundary = [s]
    parents = [None] * len(graph)
    vertex = 0
    while len(boundary) > 0:
        v = boundary.pop()
        visited += [v]
        for w in neighbours(v, graph):
            if w not in visited and w not in boundary:
                boundary.append(w)
                parents[w] = v
        if v in goals:
            vertex = v
            break
    path = deque([])
    path.append(vertex)
    while vertex != 0:
        path.appendleft(parents[vertex])
        vertex = parents[vertex]
    return path


def get_neighbours(m,  i):
    return [j for j in range(len(m[i])) if m[i][j]]


def adjacency_matrix(adj_lists):
    return [[1 if j in adj_lists[i] else 0 for j in range(len(adj_lists))] for i in range(len(adj_lists))]


def is_indset(adj_lists, a):
    if len(a) < 2:
        return True

    for x in range(len(a)-1):
        if ((a[x+1]) in adj_lists[a[x]]) and (a[x] in adj_lists[a[x+1]]):
            return False
    return True


def greedy_indset(adj_lists):
    def options(v, visited):
        total = [i for i in range(len(adj_lists))]
        removes = set()
        for x in visited:
            removes.add(x)
            for y in range(len(adj_lists[x])):
                removes.add(adj_lists[x][y])
        for x in removes:
            total.remove(x)
        return total

    smallest = min(adj_lists, key=len)
    start = adj_lists.index(smallest)
    indset = [start]
    opts = options(start, indset)
    while len(opts) > 0:
        lists = [adj_lists[i] for i in opts]
        new = adj_lists.index(min(lists, key=len))
        indset.append(new)
        opts = options(new, indset)
    return indset