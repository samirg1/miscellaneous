# dfs.py
# Date: 23-08-2022
# Author: Samir Gupta

def dfs(graph: 'list[list[int]]', /, *, start: int = 0) -> 'list[int]':
    """
    Depth-first search algorithm.
    - Input:
            - graph (list[list[int]]): The graph to search.
            - start (int, optional): The vertex to start from. Defaults to 0.
    - Returns (list[int]): The traversal list of the graph. 
    - Time Complexity: O(V+E), where V is the amount of vertexes in the graph and E is the amount of edges.
    - Aux space complexity: O(V).
    """
    visited = [not v for v in range(len(graph))] # O(V)
    stack = [start] # O(1)
    traversal: 'list[int]' = [] # O(1)
    while len(stack) > 0: # O(V+E)
        v = stack.pop() # O(1)
        traversal.append(v) # O(1)
        for adj, val in enumerate(graph[v]):
            if val and not visited[adj]: # O(1)
                stack.append(adj) # O(1)
                visited[adj] = True # O(1)
    return traversal




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

    print(dfs(graph))

if __name__ == '__main__':
    main()