# dijkstra.py
# Date: 23-08-2022
# Author: Samir Gupta

import heapq
from math import inf
from queue import PriorityQueue

def dijkstra(graph: 'list[list[int]]', /, *, start: int = 0) -> 'tuple[list[int|float], list[int]]':
    """
    Dijstra's algorithm for finding single-sourced shortest path to multiple targets.
    - Input:
            - graph (list[list[int]]): The graph to search for.
            - start (int, optional): The source vertex. Defaults to 0.
    - Returns (tuple[list[int], list[int]]): Distance array where distance[i] is the shortest distance from vertex i to the source, and parent array, where parent[i] is the next vertex to go to from i to get to source. 
    - Time Complexity: O(ElogV), where E is the amount of edges in the graph and V is the amount of vertexes.
    - Aux space complexity: O(E).
    """
    distance = [inf if v else 0 for v in range(len(graph))] # O(V)
    visited = [not v for v in range(len(graph))] # O(V)
    parent = [start for _ in graph] # O(V)
    
    heap_q: list = [(dist, i) for i, dist in enumerate(distance)] # O(V)
    heapq.heapify(heap_q) # O(V)
        
    for _ in graph: # O(ElogV)
        current = heapq.heappop(heap_q)[1]
        visited[current] = True # O(1)
        for adj, weight in enumerate(graph[current]):
            new_weight = weight + distance[current]
            if weight and not visited[adj] and new_weight < distance[adj]: # O(1)
                heapq.heappush(heap_q, (new_weight, adj)) # O(logV)
                distance[adj] = new_weight # O(1)
                parent[adj] = current # O(1)
    return distance, parent

def main():
    graph = [
        [0, 10, 5, 0, 0],
        [0,  0, 2, 1, 0],
        [0,  3, 0, 9, 2],
        [0,  0, 0, 0, 4],
        [0,  0, 0, 6, 0]
    ]
    print(dijkstra(graph))

if __name__ == '__main__':
    main()