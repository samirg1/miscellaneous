# circulation_demands.py
# Date: 28-09-2022
# Author: Samir Gupta

from math import inf

from ford_fulkerson import ford_fulkerson


class NetworkNode:
    """
    Network node to keep track of the specifc names and demands of each node.
    """

    def __init__(self, name: str, demand: int):
        """
        Initialises the node.
        - Input:
            - name (str): The name of the node.
            - demand (int): The demand of the node.
        - Time Complexity: O(1).
        - Aux space complexity: O(1).
        """
        self.name = name
        self.demand = demand

    def copy(self) -> "NetworkNode":
        return NetworkNode(**self.__dict__)

    def __repr__(self) -> str:
        return f"NetworkNode({self.name}, {self.demand})"


def circulation_demands(nodes: list[NetworkNode], graph: list[list[int]], lower_bound: int = 0) -> list[list[int]] | None:
    """
    Finds a feasible solution to the circulation with demands problem or returns None.
    - Input:
        - nodes (list[NetworkNode]): The nodes in the network.
        - graph (list[list[int]]): The graph representing the network.
        - lower_bound (int, optional): The lower bound of flow. Defaults to 0.
    - Returns (list[list[int]] | None): The solution graph or None if there isn't one.
    - Time Complexity: O(VE^2), where V is the amount of vertexes in the graph and E is the amount of edges.
    - Aux space complexity: O(VE^2).
    """
    if lower_bound == 0:  # return the simple solution if there is no lower bound
        return _circulation_demands_aux(nodes, graph)  # O(VE^2)

    # find minimum capacity (doesn't include zeroes) O(V^2)
    min_cap = min([min(row, key=lambda v: inf if v == 0 else v) for row in graph], key=lambda v: inf if v == 0 else v)

    if lower_bound > min_cap:  # ensure lower_bound is not over the minimum capacity
        raise ValueError("Lower bound cannot be greater than the minimum capacity of nodes")

    # initialise the two graphs to split into to solve the lower bounded solution
    fixed_flow = [row.copy() for row in graph]  # O(V^2)
    reduced_graph = [row.copy() for row in graph]  # O(V^2)
    new_nodes = [node.copy() for node in nodes]  # O(V)

    for i, row in enumerate(graph):  # O(V^2)
        for j, val in enumerate(row):
            if val:
                fixed_flow[i][j] = lower_bound  # set the lower bound as fixed flow
                reduced_graph[i][j] -= lower_bound  # reduce the lower bound from the capactity
                new_nodes[i].demand += lower_bound  # add the lower bound to the start node
                new_nodes[j].demand -= lower_bound  # subtract the lower bound from the end node

    max_reduced = _circulation_demands_aux(new_nodes, reduced_graph)  # get the solution to the reduced problem

    if max_reduced is None:
        return None # if there is no solution then there is no solutoin to the bigger problem

    for i, row in enumerate(fixed_flow): # otherwise add the fixed flow back
        for j, val in enumerate(row):
            max_reduced[i][j] += val

    return max_reduced


def _circulation_demands_aux(nodes: list[NetworkNode], graph: list[list[int]]) -> list[list[int]] | None:
    """
    Auxilary function for finding a feasible circulation with demands network solution if there is one.
    - Input:
        - nodes (list[NetworkNode]): List of network nodes in the network.
        - graph (list[list[int]]): The graph of the network.
    - Returns (list[list[int] | None]): The feasible graph solution or None and 0 if there isn't one.
    - Time Complexity: O(VE^2), where V is the amount of vertexes in the graph and E is the amount of edges.
    - Aux space complexity: O(VE^2).
    """
    graph_ = [[0] * (len(graph) + 2)] + [[0, *row.copy(), 0] for row in graph] + [[0] * (len(graph) + 2)]  # create space for source and sink node O(V^2)

    outgoing_caps = [0] * (len(graph) + 2)  # keep track of capacities of outgoing source edges O(V)

    for i, node in enumerate(nodes, start=1):  # add source and sink node edge values O(V)
        if node.demand < 0:
            graph_[0][i] = -node.demand
            outgoing_caps[i] = -node.demand
        elif node.demand > 0:
            graph_[i][-1] = node.demand

    _, solution = ford_fulkerson(graph_)  # O(VE^2)
    for cap, val in zip(outgoing_caps, solution[0]):  # O(V)
        if cap != val:  # if max capacity of outgoing source is not upheld
            return None

    solution = [row[1:-1] for row in solution][1:-1]  # remove source and sink node O(V^2)

    return solution


def main():
    nodes = [NetworkNode("x", -4), NetworkNode("y", -3), NetworkNode("z", 0), NetworkNode("v", 2), NetworkNode("w", 5)]
    graph = [[0, 3, 0, 3, 0], [0, 0, 0, 2, 3], [0, 2, 0, 0, 0], [0, 0, 0, 0, 2], [0, 0, 2, 0, 0]]

    nodes2 = [NetworkNode("x", -4), NetworkNode("u", -3), NetworkNode("v", 2), NetworkNode("w", 5)]
    graph2 = [
        [0, 3, 3, 0],
        [0, 0, 2, 3],
        [0, 0, 0, 2],
        [0, 0, 0, 0],
    ]
    assert circulation_demands(nodes, graph) == [[0, 1, 0, 3, 0], [0, 0, 0, 1, 3], [0, 0, 0, 0, 0], [0, 0, 0, 0, 2], [0, 0, 0, 0, 0]]
    assert circulation_demands(nodes, graph, 1) is None
    assert circulation_demands(nodes2, graph2) == [[0, 1, 3, 0], [0, 0, 1, 3], [0, 0, 0, 2], [0, 0, 0, 0]]
    assert circulation_demands(nodes2, graph2, 2) == [[0, 2, 2, 0], [0, 0, 2, 3], [0, 0, 0, 2], [0, 0, 0, 0]]
    try:
        circulation_demands(nodes2, graph2, 3)
    except ValueError:
        ...


if __name__ == "__main__":
    main()
