from math import inf

VERTEX = list[int|float]
ADJ_MATRIX = list[VERTEX]

class NegativeCycleError(ValueError):
    """
    Inappropriate graph passed in with negative cycles.
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def floyd_warshall(graph: ADJ_MATRIX) -> ADJ_MATRIX:
    """
    Floyd-Warshall's algorithm for finding the shortest path from all vertices to all other vertices.
    - Input:
            - graph (ADJ_MATRIX): Adjacency matrix representation of the graph.
    - Returns (ADJ_MATRIX): An adjacency matrix where matrix[i][j] represents the shortest distance from vertex i to vertex j. 
    - Time Complexity: O(V^3) where V is the amount of vertices in the graph.
    - Aux space complexity: O(V^2).
    """
    distance: ADJ_MATRIX = [[graph[i][j] if i == j or graph[i][j] != 0 else inf for j in range(len(graph))] for i in range(len(graph))] # O(V^2)
            
    for v in range(len(graph)): # O(V^3)
        for i in range(len(graph)): # O(V^2)
            for j in range(len(graph)): # O(V)
                distance[i][j] = min(distance[i][j], distance[i][v] + distance[v][j]) # O(1)
                
    for v in range(len(graph)): # O(V)
        if distance[v][v] < 0:
            raise NegativeCycleError()
        
    return distance

def main():
    graph1 = [ # graph from lectures
        [0, 10, -2, 0],
        [4,  0, 3, 0],
        [0,  0, 0, 2],
        [0,  -1, 0, 0],
    ] 
    graph2 = [ # graph from lectures with negative cycles
        [0, 10, -2, 0],
        [6,  0, 2, 0],
        [0,  0, 0, -2],
        [0,  -1, 0, 0],
    ] 
    for row in floyd_warshall(graph1):
        print(row)

if __name__ == '__main__':
    main()