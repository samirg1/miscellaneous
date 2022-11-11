# bipartite_matching.py
# Date: 28-09-2022
# Author: Samir Gupta

from abc import abstractmethod
from typing import Protocol

from ford_fulkerson import ford_fulkerson


class _SupportsDunderInt(Protocol):
    @abstractmethod
    def __int__(self) -> int:
        ...


def bipartite_matching_max(edges: list[tuple[_SupportsDunderInt, _SupportsDunderInt]]) -> int:
    """
    Uses the Fork-Fulkerson algorithm to find the maximum amount of matches that can occur in a bipartite set.
    - Input:
        - edges (list[tuple[_SupportsDunderInt, _SupportsDunderInt]]): The edges in the bipartite set with vertexes starting at 1.
    - Returns (int): The maximum amount of matches.
    - Time Complexity: O(VE^2), where V is the amount of vertices and E is the amount of edges in the bipartite set.
    - Aux space complexity: O(VE^2).
    """
    links = [(int(to), int(fro)) for to, fro in edges]  # convert all values to integers O(E)
    _, max_r = max(links, key=lambda link: max(link[0], link[1]))  # find max edge O(E)
    graph_rows = max_r + 2  # add two rows for the start and end vertex
    graph = [[0] * (graph_rows) for _ in range(graph_rows)]  # O(V^2)
    for to, fro in links:  # O(E)
        if to < 1:  # make sure min index is 1
            raise ValueError("Vertex id's must start at 1")
        graph[0][to] = 1  # source vertex can travel to any of the starting vertices
        graph[to][fro] = 1  # adding the edges
        graph[fro][-1] = 1  # all end vertexes point to the sink vertex

    max_flow, _ = ford_fulkerson(graph)  # O(VE^2)
    return max_flow


def main():
    edges: list[tuple[_SupportsDunderInt, _SupportsDunderInt]] = [
        (1, 6),
        (2, 6),
        (2, 8),
        (3, 7),
        (3, 8),
        (3, 9),
        (4, 8),
        (5, 8),
    ]
    print(bipartite_matching_max(edges))


if __name__ == "__main__":
    main()
