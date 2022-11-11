# bfs.py
# Date: 23-08-2022
# Author: Samir Gupta

from queue import Queue

def bfs(graph: list[list[int]], /, *, start: int = 0) -> tuple[list[int], list[int], list[int]]:
    """
    Breadth-first search algorithm.
    - Input:
            - graph (list[list[int]]): Adjacency matrix of the graph to search in.
            - start (int, optional): The starting vertex. Defaults to 0. Use start= to specify a non-zero vertex to start from.
    - Returns (tuple[list[int], list[int], list[int]]): Three lists, 
            - visited, the list of vertexes in the order by which they were traversed.
            - distance, where distance[i] is the distance from the i'th vertex to the starting vertex.
            - predecessor, such that predecessor[i] is the next vertex to travel to when starting at i and going to start. 
    - Time Complexity: O(V+E), where V is the amount of vertices and E is the amount of edges in the graph.
    - Aux space complexity: O(V).
    """
    distance: list[int] = [len(graph) for _ in graph] # O(V)
    predecessors: list[int] = [start for _ in graph] # O(V)
    queue: Queue = Queue(len(graph)-1) # O(1)
    visited: list[int] = [start]
    queue.put(start) # O(1)
    distance[start] = 0 # O(1)
    while not queue.empty(): # O(V+E)
        current = queue.get() # O(1)
        for adj, val in enumerate(graph[current]):
            if val and distance[adj] == len(graph): # O(1)
                visited.append(adj) # O(1)
                distance[adj] = distance[current] + val # O(1)
                predecessors[adj] = current # O(1)
                queue.put(adj) # O(1)
                    
    return visited, distance, predecessors

def shortest_path(graph: list[list[int]], to: int, /, *, start: int = 0) -> list[int]:
    """
    Finds the shortest path between two vertices in an unweighted graph.
    - Input:
            - graph (list[list[int]]): The adjacency matrix representation of a graph.
            - end (int): The end vertex.
            - start (int, optional): The start vertex (keyword only). Defaults to 0. 
    - Returns (list[int]): A list of vertexes, where list[i] is the vertex to start from, list[i+1] is the next vertex and so on until list[-1] == end vertex. 
    - Time Complexity: O(V+E), where V is the amount of vertexes in the graph and E is the amount of edges.
    - Aux space complexity: O(V).
    """
    *_, pred = bfs(graph, start=start) # O(V+E)
    path: list[int] = [to] # O(1)
    current = to # O(1)
    while current != start: # O(V) as len(path) is in O(V)
        u = pred[current] # O(1)
        path.append(u) # O(1)
        current = u # O(1)
    return path[::-1] # O(V)
        
def main():
    graph = [ # graph shown in lectures
        [0, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 1],
        [0, 0, 0, 0, 1, 0, 1, 0]
    ]
    graph2 = [ # graph with biggest queue size (A connected to everything else)
        [0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0]
    ]
    graph3 = [ # single line graph (like a linked list)
        [0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0]
    ]

    print(f'{bfs(graph3) = }')
    print(f'{shortest_path(graph3, 0) = }')

if __name__ == '__main__':
    main()
