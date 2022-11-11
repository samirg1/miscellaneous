from math import inf

ADJACENT_VERTEX = tuple[int, int]
VERTEX = list[ADJACENT_VERTEX]
ADJ_LIST = list[VERTEX]

class NegativeCycleError(ValueError):
    """
    Inappropriate graph passed in with negative cycles.
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def bellman_ford(graph: ADJ_LIST, source: int) -> tuple[list[int|float], list[int|None]]:
    """
    Bellman-Ford's algorithm for a shortest single sourced path to multiple targets with negative weights.
    - Input:
            - graph (ADJ_LIST): Adjacency list representation of the graph.
            - source (int): The source node.
    - Returns (tuple[list[int|float], list[int|None]]): 
        - distance: where distance[i] is the shortest distance from source to i.
        - parent: where parent[i] is the next node after i to travel from i to source. 
    - Time Complexity: O(VE) where V is the amount of vertices in the graph and E is the amount edges.
    - Aux space complexity: O(V).
    """
    distance: list[int|float] = [inf for _ in graph]
    parent: list[int|None] = [None for _ in graph]
    distance[source] = 0
    
    for _ in range(len(graph)-1):
        for u in range(len(graph)):
            for v, w in graph[u]:
                if (est := distance[u] + w) < distance[v]:
                    distance[v], parent[v] = est, u
                    
    for u in range(len(graph)):
        for v, w in graph[u]:
            if distance[u] + w < distance[v]:
                raise NegativeCycleError()                

    return distance, parent