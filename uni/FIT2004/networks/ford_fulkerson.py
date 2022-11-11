# ford-fulkerson.py
# Date: 28-09-2022
# Author: Samir Gupta

from math import inf
from queue import Queue
from typing import cast


def searching_bfs(graph: list[list[int]], start: int, target: int, parent: list[int] | None = None) -> tuple[bool, list[int]]:
    """
    Use BFS to search for a target from a source.
    - Input:
            - graph (list[list[int]]): The graph to search in.
            - start (int): The starting node.
            - target (int): The target node.
            - parent (list[int], optional): Optional parent array to pass in to modify in place otherwise one is created.
    - Returns (tuple[bool, list[int]]): Boolean representing if the target can be reached from start and a parent array where parent[i] is the next node from i to target.
    - Time Complexity: O(V+E), where V is the amount of vertices in the graph and E is the amount of edges.
    - Aux space complexity: O(V+E).
    """
    parent = [-1] * len(graph) if parent is None else parent  # O(V)
    visited = [False] * len(graph)  # O(V)
    queue: Queue[int] = Queue()

    queue.put(start)
    visited[start] = True

    while not queue.empty():  # O(V+E)
        current = queue.get()
        for adj, val in enumerate(graph[current]):
            if val and not visited[adj]:
                queue.put(adj)
                visited[adj] = True
                parent[adj] = current

    return visited[target], parent


def ford_fulkerson(graph: list[list[int]], /, *, source: int | None = None, sink: int | None = None) -> tuple[int, list[list[int]]]:
    """
    Ford-Fulkerson algorithm to find the maximum flow in a graph.
    - Input:
        - graph (list[list[int]]): The graph representing the network.
        - source (int, optional): The source vertex. Defaults to 0.
        - sink (int, optional): The sink/target vertex. Defaults to len(graph)-1
    - Returns (tuple[int, list[list[int]]): The maximum flow of the network and the maximum flow solution.
    - Time Complexity: O(VE^2), where V is the amount of vertices in the graph and E is the amount of edges.
    - Aux space complexity: O(VE^2).
    """
    residual = [row.copy() for row in graph] # copy graph for residuals
    solution = [[0] * len(residual) for _ in residual] # solution graph
    
    source = 0 if source is None else source # default the source node
    sink = len(residual) - 1 if sink is None else sink # default the sink node
    
    max_flow = 0
    
    path_found, parent = searching_bfs(residual, source, sink)  # O(E)
    while path_found:  # O(EV)
        path_flow: int | float = inf
        s = sink
        while s != source:  # find minimum flow increase along path O(V)
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]

        v = sink
        while v != source:  # update residual values of edges O(V)
            u = parent[v]
            residual[u][v] -= int(path_flow)
            residual[v][u] += int(path_flow)
            solution[u][v] += cast(int, path_flow) # update solution
            v = parent[v]

        max_flow += cast(int, path_flow)  # add the path flow
        path_found, parent = searching_bfs(residual, source, sink)  # O(E)

    return max_flow, solution


def main():
    graph = [[0, 16, 13, 0, 0, 0], [0, 0, 10, 12, 0, 0], [0, 4, 0, 0, 14, 0], [0, 0, 9, 0, 0, 20], [0, 0, 0, 7, 0, 4], [0, 0, 0, 0, 0, 0]]
    graph2 = [[0, 3, 5, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 5, 0], [0, 0, 3, 0, 0, 3], [0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0]]
    
    print(ford_fulkerson(graph))
    #assert ford_fulkerson(graph) == (23, [[0, 12, 7, 0, 0, 0], [0, 0, 0, 12, 0, 0], [0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 7], [0, 0, 0, 7, 0, 4], [0, 0, 0, 0, 0, 0]])
    #assert ford_fulkerson(graph2) == (8, [[0, 3, 5, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0]])
    
    graph3 = [[0, 4, 3, 0, 0, 0, 0], [0, 0, 3, 0, 3, 0, 0], [0, 0, 0, 0, 2, 3, 0], [0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2], [0, 0, 0, 2, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0]]
    print(ford_fulkerson(graph3))


if __name__ == "__main__":
    main()
