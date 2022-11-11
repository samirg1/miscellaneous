# prims.py
# Date: 23-08-2022
# Author: Samir Gupta

from queue import PriorityQueue
from math import inf

def prims(graph: 'list[list[int]]', /, *, start: int = 0) -> 'list[tuple[int, int]]':
    """
    Prim's algorithm for a MST.
    - Input:
            - graph (list[list[int]]): Graph to find MST of.
            - start (int, optional): Start vertex of the MST. Defaults to 0.
    - Returns (list[tuple[int, int]]): List of edges (a, b), where a is the start vertex and b is the connected vertex. 
    - Time Complexity: O(ElogV), where E is the amount of edges in the graph and V is the amount of vertexes.
    - Aux space complexity: O(E).
    """
    distance = [inf if v else 0 for v in range(len(graph))] # O(V)
    parent = [start for _ in graph] # O(V)
    visited = [not v for v in range(len(graph))] # O(V)
    edges: list[tuple[int, int]] = [] # O(1)
    queue: PriorityQueue = PriorityQueue() # O(1)
    for i, dist in enumerate(distance): queue.put((dist, i))  # O(ElogV)
    
    for _ in graph: # (ElogV)
        current = queue.get()[1] # O(1)
        visited[current] = True # O(1)
        edges.append((parent[current], current)) # O(1)
        for adj, weight in enumerate(graph[current]):
            if weight and not visited[adj] and weight < distance[adj]: # O(1)
                queue.put((weight, adj)) # O(logV)
                distance[adj] = weight # O(1)
                parent[adj] = current # O(1)
    return edges[1:] # O(E)


def main():
    graph = [
        [0, 10, 5, 0, 0],
        [10, 0, 3, 1, 0],
        [5,  3, 0, 9, 2],
        [0,  1, 9, 0, 6],
        [0,  0, 2, 6, 0]
    ]
    print(prims(graph))

if __name__ == '__main__':
    main()