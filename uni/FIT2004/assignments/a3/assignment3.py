# assignment3.py
# Date: 09-10-2022
# Author: Samir Gupta

'''
NOTE:
For task 1, majority of test cases don't work, but I believe my solution works except one minor flaw in my Ford-Fulkerson /
searching_bfs algorithms as for some reason they are adding flow between restuarants and people/selectors.
I'm hoping I can receive some consequential marks for this.
'''

from __future__ import annotations

from math import inf
from queue import Queue
from typing import Iterator, cast


class NetworkNode:
    '''
    Network node to keep track of the specifc names and demands of each node.
    '''

    def __init__(self, name: str, demand: int):
        '''
        Initialises the node.
        - Input:
            - name (str): The name of the node.
            - demand (int): The demand of the node.
        - Time Complexity: O(1).
        - Aux space complexity: O(1).
        '''
        self.name = name
        self.demand = demand

    def __repr__(self) -> str:
        return f'NetworkNode({self.name}, {self.demand})'

    def copy(self) -> NetworkNode:
        '''
        Copy the network node to return a new instance.
        - Returns (NetworkNode): The new instance.
        - Time Complexity: O(1).
        - Aux space complexity: O(1).
        '''
        return NetworkNode(**self.__dict__)


class FlowEdge:
    '''
    Object to represent a flow edge with lower and upper bounds.
    '''

    def __init__(self, lb: int = 0, ub: int = 0, flow: int = 0) -> None:
        '''
        Initialise the flow edge.
        - Input:
            - lb (int, optional): The lower bound of the flow edge. Defaults to 0.
            - ub (int, optional): The upper bound of the flow edge. Defaults to 0.
            - flow (int, optional): The flow flowing through this edge. Defaults to 0.
        - Time Complexity: O(1).
        - Aux space complexity: O(1).
        '''
        self.lb = lb
        self.ub = ub
        self.flow = flow

    def __repr__(self) -> str:
        if self.flow == 0 and self.lb == 0 and self.ub == 0:
            return '-----'
        return f'{self.flow}/{self.lb}/{self.ub}'

    def __bool__(self) -> bool:  # 'if FlowEdge' returns true if there is an upper bound
        return bool(self.ub)

    def copy(self) -> FlowEdge:
        '''
        Copy the flow edge to return a new instance.
        - Returns (FlowEdge): The new instance.
        - Time Complexity: O(1).
        - Aux space complexity: O(1).
        '''
        return FlowEdge(**self.__dict__)


def searching_bfs(graph: list[list[FlowEdge]], start: int, target: int) -> tuple[bool, list[int]]:
    '''
    Use BFS to search for a target from a source.
    - Input:
            - graph (list[list[FlowEdge]]): The graph to search in.
            - start (int): The starting node.
            - target (int): The target node.
            - parent (list[int], optional): Optional parent array to pass in to modify in place otherwise one is created.
    - Returns (tuple[bool, list[int]]): Boolean representing if the target can be reached from start and a parent array where parent[i] is the next node from i to target.
    - Time Complexity: O(V+E), where V is the amount of vertices in the graph and E is the amount of edges.
    - Aux space complexity: O(V+E).
    '''
    parent = [-1] * len(graph)  # O(V)
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


def ford_fulkerson(graph: list[list[FlowEdge]], /, *, source: int | None = None, sink: int | None = None) -> tuple[int, list[list[FlowEdge]]]:
    '''
    Ford-Fulkerson algorithm to find the maximum flow in a graph.
    - Input:
        - graph (list[list[FlowEdge]]): The graph representing the network.
        - source (int, optional): The source vertex. Defaults to 0.
        - sink (int, optional): The sink/target vertex. Defaults to len(graph)-1
    - Returns (tuple[int, list[list[FlowEdge]]): The maximum flow of the network and the maximum flow solution.
    - Time Complexity: O(EF), where E is the amount of edges in the network and F is the maximum flow.
    - Aux space complexity: O(EF).
    '''
    residual = [[edge.copy() for edge in row] for row in graph]  # copy graph for residuals
    solution = [[FlowEdge(edge.lb, edge.ub, 0) for edge in row] for row in graph]  # solution graph

    source = 0 if source is None else source  # default the source node
    sink = len(residual) - 1 if sink is None else sink  # default the sink node

    max_flow = 0

    path_found, parent = searching_bfs(residual, source, sink)  # O(E)
    while path_found:  # O(EF)
        path_flow: int | float = inf
        s = sink
        while s != source:  # find minimum flow increase along path O(V)
            path_flow = min(path_flow, residual[parent[s]][s].ub)
            s = parent[s]

        v = sink
        while v != source:  # update residual values of edges O(V)
            u = parent[v]
            residual[u][v].ub -= int(path_flow)
            residual[v][u].ub += int(path_flow)
            solution[u][v].flow += cast(int, path_flow)  # update solution
            v = parent[v]

        max_flow += cast(int, path_flow)  # add the path flow
        path_found, parent = searching_bfs(residual, source, sink)  # O(E)

    return max_flow, solution


def circulation_demands(graph: list[list[FlowEdge]], nodes: list[NetworkNode]) -> list[list[FlowEdge]] | None:
    '''
    Solve a circulation with demands problem that contains lower bounds.
    - Input:
        - graph (list[list[FlowEdge]]): The network to solve.
        - nodes (list[NetworkNode]): The nodes in the network (with demand).
    - Returns (list[list[FlowEdge]] | None): The solution to the network if there is one.
    - Time Complexity: O(EF), where E is the amount of edges in the network and F is the maximum amount of flow.
    - Aux space complexity: O(EF).
    '''
    # initialise the two graphs to split into to solve the lower bounded solution
    fixed_flow = [[0 for _ in row] for row in graph]  # O(V^2)
    reduced_graph = [[edge.copy() for edge in row] for row in graph]  # O(V^2)
    new_nodes = [node.copy() for node in nodes]  # O(V)

    for i, row in enumerate(graph):  # O(V^2)
        for j, val in enumerate(row):
            if val:
                fixed_flow[i][j] = val.lb  # set the lower bound as fixed flow
                reduced_graph[i][j].ub -= val.lb  # reduce the lower bound from the capactity
                reduced_graph[i][j].lb -= val.lb
                new_nodes[i].demand += val.lb  # add the lower bound to the start node
                new_nodes[j].demand -= val.lb  # subtract the lower bound from the end node

    max_reduced = _circulation_demands_aux(reduced_graph, new_nodes)  # get the solution to the reduced problem O(EF)

    if max_reduced is None:
        return None  # if there is no solution then there is no solutoin to the bigger problem

    for i, r in enumerate(fixed_flow):  # otherwise add the fixed flow back
        for j, flow in enumerate(r):
            max_reduced[i][j].flow += flow

    return max_reduced


def _circulation_demands_aux(graph: list[list[FlowEdge]], nodes: list[NetworkNode]) -> list[list[FlowEdge]] | None:
    '''
    Auxilary function for finding a feasible circulation with demands network solution if there is one.
    - Input:
        - graph (list[list[FlowEdge]]): The graph of the network.
        - nodes (list[NetworkNode]): List of network nodes in the network.
    - Returns (list[list[FlowEdge] | None]): The feasible graph solution or None and 0 if there isn't one.
    - Time Complexity: O(EF), where E is the amount of edges in the network and F is the maximum amount of flow.
    - Aux space complexity: O(EF).
    '''
    graph_ = [[FlowEdge() for _ in range((len(graph) + 2))]] + [[FlowEdge(), *[edge.copy() for edge in row], FlowEdge()] for row in graph] + [[FlowEdge()] * (len(graph) + 2)]  # create space for source and sink node O(V^2)
    outgoing_caps = [0] * (len(graph) + 2)  # keep track of capacities of outgoing source edges O(V)

    for i, node in enumerate(nodes, start=1):  # add sour
        if node.demand < 0:
            graph_[0][i].ub = -node.demand
            outgoing_caps[i] = -node.demand
        elif node.demand > 0:
            graph_[i][-1].ub = node.demand

    _, solution = ford_fulkerson(graph_)  # O(EF)
    for cap, val in zip(outgoing_caps, solution[0]):  # O(V)
        if cap != val.flow:  # if max capacity of outgoing source is not upheld
            return None

    solution = [row[1:-1] for row in solution][1:-1]  # remove source and sink node O(V^2)

    return solution


class HouseMateMealNetwork:
    '''
    Class to represent the housemate meal network.
    '''

    def __init__(self, availability: list[list[int]]) -> None:
        '''
        Initialise the network.
        - Input:
            - availability (list[list[int]]): The list of housemate availabilities.
        - Time Complexity: O(n^2), where n is the amount of date to allocate for.
        - Aux space complexity: O(n^2).
        '''
        self.availability = availability

        # constants for reuse
        self.DAYS = len(self.availability)
        self.MEALS = self.DAYS * 2
        self.PEOPLE = len(self.availability[0])
        self.SELECTORS = self.DAYS * self.PEOPLE
        self.MEAL_LB = int(0.36 * self.DAYS)  # meal lower bound O(1)
        self.MEAL_UB = int(0.44 * self.DAYS) + 1  # meal upper bound O(1)
        self.REST_MAX = int(0.1 * self.DAYS)  # restuarant upper bound O(1)

        # nodes in the graph
        self.nodes = (
            [NetworkNode('Source', 0)]  # source node
            + [NetworkNode(f'{i}', 0) for i in range(self.PEOPLE)]  # node for each person
            + [NetworkNode('Restuarant', 0)]  # node for resturant
            + [NetworkNode(f'Selector_{i}_{j}', 0) for i in range(self.PEOPLE) for j in range(self.DAYS)]  # node for a selector for each day
            + [NetworkNode(f'Breakfast_{i//2}', 0) if not i % 2 else NetworkNode(f'Dinner_{i//2}', 0) for i in range(self.MEALS)]  # node for each meal
            + [NetworkNode('Feedback', 0)]  # node for the feedback
        )

        self.graph = self._create_circulation_graph()  # create the circulation graph from availabilty O(n^2)

    def _create_circulation_graph(self) -> list[list[FlowEdge]]:
        '''
        Create the circulation graph to be solved from housemate availabilites.
        - Returns (list[list[FlowEdge]]): Circulation graph.
        - Time Complexity: O(n^2), where n is the amount of days to share meals for. (This is due to len(availability[i]) is constant for each i = 5 housemates)
        - Aux space complexity: O(n^2).
        '''
        graph = [[FlowEdge() for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]  # initialise graph O(n^2) as size is in O(n) as self.PEOPLE is constant

        graph[0][self.PEOPLE + 1] = FlowEdge(0, self.REST_MAX)  # set the restuarant FlowEdge O(1)

        for day_num, day in enumerate(self.availability):  # O(n)
            breakfast_index = 2 + self.PEOPLE + day_num * 2 + self.SELECTORS  # index of the breakfast node on day O(1)
            dinner_index = breakfast_index + 1  # index of the dinner node on day O(1)

            # restuarant can used for any meal
            graph[self.PEOPLE + 1][breakfast_index] = FlowEdge(0, 1)  # O(1)
            graph[self.PEOPLE + 1][dinner_index] = FlowEdge(0, 1)  # O(1)

            graph[breakfast_index][-1] = FlowEdge(1, 1)  # add outgoing each for breakfasts O(1)
            graph[dinner_index][-1] = FlowEdge(1, 1)  # add outgoing each for dinners O(1)

            for hm_num, avail_num in enumerate(day):  # O(1) as the amount of people is constant (5)
                selector_i = self.PEOPLE + 2 + hm_num * 2 + day_num  # index of the selector fo the person on the day

                graph[0][hm_num + 1] = FlowEdge(self.MEAL_LB, self.MEAL_UB)  # add min and max from source to each person O(1)

                if avail_num in (1, 3):  # can do breakfast
                    graph[hm_num + 1][selector_i] = FlowEdge(0, 1)  # O(1)
                    graph[selector_i][breakfast_index] = FlowEdge(0, 1)

                if avail_num in (2, 3):  # can do dinner
                    graph[hm_num + 1][selector_i] = FlowEdge(0, 1)  # O(1)
                    graph[selector_i][dinner_index] = FlowEdge(0, 1)

        sum_lb = self.PEOPLE * self.MEAL_LB  # get sum of lower bounds O(1)
        sum_ub = self.REST_MAX + self.PEOPLE * self.MEAL_UB  # get sum of upper bounds O(1)
        graph[-1][0] = FlowEdge(sum_lb, sum_ub)  # create circulation with extra edge O(1)

        # print(graph)
        return graph

    def get_allocations(self) -> tuple[list[int], list[int]] | None:
        '''
        Get the allocations for each meal if there is a valid solution.
        - Returns (tuple[list[int], list[int]] | None): The allocations or None is there is no solution.
        - Time Complexity: O(n^2), where n is the amount of days to allocate for.
        - Aux space complexity: O(n^2).
        '''
        # solve the network O(n^2)
        # as the maximum amount of flow is 2*n (the amount of meals)
        # and the amount of edges = is in O(n),
        # therefore O(n^2) total complexity.
        solution = circulation_demands(self.graph, self.nodes)
        if solution is None:
            return None

        allocations: tuple[list[int], list[int]] = ([], [])  # initialise the allocations array O(1)

        # loop over each column of the graph matrix and find the housemate who has been allocated each meal
        for i in range(self.DAYS):  # O(n^2)
            breakfast_index = i * 2 + self.PEOPLE + 2 + self.SELECTORS  # breakfast meal index
            dinner_index = breakfast_index + 1  # dinner meal index

            rest_index = 1 + self.PEOPLE  # check if the restuarant was assigned any meals
            if solution[rest_index][breakfast_index].flow:  # if the restuarant was allocated to breakfast
                allocations[0].append(self.PEOPLE)  # add restuarant to breakfast array
            elif solution[rest_index][dinner_index].flow:  # if the restuarant was allocated to dinner
                allocations[1].append(self.PEOPLE)  # add restuarant to dinner array
            else:
                for j in range(self.SELECTORS // 2):  # loop over each selector row
                    k = j * 2 + self.PEOPLE + 2 + i
                    if solution[k][breakfast_index].flow:  # if this housemate was allocated to breakfast
                        allocations[0].append(j)  # add housemate to breakfast array
                    elif solution[k][dinner_index].flow:  # if this housemate was allocated to dinner
                        allocations[1].append(j)  # add housemate to dinner array

        return allocations


def allocate(availability: list[list[int]]) -> tuple[list[int], list[int]] | None:
    '''
    Allocate meals to housemates fairly.
    - Input:
        - availability (list[list[int]]): List of availability for each day.
    - Returns (tuple[list[int], list[int]] | None): None if there is no solution or two lists:
        - breakfast: where breakfast[i] = the housemate number of the housemate preparing that breakfast
        - dinner: where dinner[i] = the housemate number of the housemate preparing that dinner
    - Time Complexity: O(n^2), where n is the amount of days to allocate meals.
    - Aux space complexity: O(n^2).
    '''
    network = HouseMateMealNetwork(availability)
    return network.get_allocations()


class SuffixTree:
    '''
    Representation of a suffix tree using a suffix array for all lower case alphabetic (and space) strings.
    '''

    class SuffixTreeNode:
        '''
        Node contained in the suffix tree.
        '''

        def __init__(self, string: str = '', children: list[int] | None = None, /, *, total_esc: int):
            '''
            Initialise the suffix tree node.
            - Input:
                - total_esc (int): The total amount of escaping characters present in the tree.
                - string (str, optional): The string represented by this node. Defaults to ''.
                - children (list[int] | None, optional): The list of indicies of child nodes of this node. Defaults to None.
            - Time Complexity: O(n), where n is the amount of escaping characters in the suffix tree.
            - Aux space complexity: O(n).
            '''
            self.string = string
            self.children = children or []  # initialise children
            self.marks = [''] * total_esc  # initialise marks array

    def __init__(self, *strings: str):
        '''
        Initialise the suffix tree.
        - Input:
            - *strings (str): Any number of strings to add to the suffix tree
        - Time Complexity: O(n*s^2), where n is the number of string and s is the sum of the lengths of the strings.
        - Aux space complexity: O(n*s^2).
        '''
        self.nodes = [self.SuffixTreeNode(total_esc=len(strings))]  # initialise head node in array
        self._strings = strings
        self._add_strings()  # add strings to tree O(n*s^2)
        self._mark_tree(self.nodes[0])  # mark the tree O(n*s)

    def _add_strings(self):
        '''
        Add the suffix tree's strings into the tree .
        - Time Complexity: O(n*s^2), where n is the number of string and s is the sum of the lengths of the strings.
        - Aux space complexity: O(n*s^2).
        '''
        for i, string in enumerate(self._strings):  # O(n*s^2)
            string += f'{i}'  # add null character unique to each string
            self.curr_suffixes = [string[i:] for i in range(len(string))]

            for suff_no, suffix in enumerate(self.curr_suffixes):  # O(s^2)
                self._add_string_suffix(suffix, suff_no)  # add each suffix

    def _add_string_suffix(self, suffix: str, suff_no: int):
        '''
        Add a string's suffix to the suffix tree.
        - Input:
            - suffix (str): The suffix to add.
            - suff_no (int): The index of the suffix in self.curr_suffixes.
        - Time Complexity: O(N), where N is the length of the suffix.
        - Aux space complexity: O(N).
        '''
        i = 0  # keep track of where we are in the string
        current_n = 0  # current node index
        while i < len(suffix):
            tree_pos = 0  # current position in the tree
            char = suffix[i]  # current character in suffix
            while True:
                children = self.nodes[current_n].children  # get the current children
                if tree_pos == len(children):  # no matching child, remainder of suffix becomes new node
                    new_n = len(self.nodes)  # get the new node index
                    self.nodes.append(self.SuffixTreeNode(self.curr_suffixes[suff_no + i], total_esc=len(self._strings)))  # add the rest of the suffix onto the nodde
                    self.nodes[current_n].children.append(new_n)  # add the new node as the child of the current one
                    return
                new_n = children[tree_pos]
                if self.nodes[new_n].string[0] == char:
                    break
                tree_pos = tree_pos + 1

            # find the common ground between the prefix of substring and child's suffix
            j = 0
            substring = self.nodes[new_n].string
            while j < len(substring):
                if suffix[i + j] != substring[j]:  # if we found the part in common
                    new_n, common_n = len(self.nodes), new_n
                    self.nodes.append(self.SuffixTreeNode(substring[:j], [common_n], total_esc=len(self._strings)))  # create the node
                    self.nodes[common_n].string = substring[j:]  # old node loses the part in common
                    self.nodes[current_n].children[tree_pos] = new_n
                    break
                j = j + 1

            i = i + j  # advance past part in common
            current_n = new_n  # continue down the tree

    def _mark_tree(self, curr: SuffixTreeNode) -> Iterator[bool]:
        '''
        Add markers to the nodes of the tree to indicate which string(s) the node's suffix belongs to.
        - Input:
            - curr (SuffixTreeNode): The current suffix node.
        - Returns (Generator[bool, None, None]): Generator of whether we have found a marker or not in curr or below.
        - Time Complexity: O(n*s), where n is the amount of strings in the tree and s is the sum of the lengths of those strings.
        - Aux space complexity: O(n*s).
        '''
        for child in curr.children:  # dfs approach
            found_gen = self._mark_tree(self.nodes[child])
            for i, found in enumerate(found_gen):  # if we have found a marker below
                if found:
                    curr.marks[i] = f'{i}'

        # return whether we have found a marker below of have a marker in curr for each marker
        return (bool(mark) or curr.string[-1] == f'{c}' for c, mark in enumerate(curr.marks))

    def longest_common_substring(self) -> str:
        '''
        Get the longest common substring between the strings in the suffix tree.
        - Returns (str): The longest common substring.
        - Time Complexity: O(s), where s is the sum of the lengths of strings inside the suffix tree.
        - Aux space complexity: O(s).
        '''
        solution = ['']  # store the lcs
        self._longest_common_substring_aux(self.nodes[0], solution)  # solve for it
        return solution[0]  # return it

    def _longest_common_substring_aux(self, curr: SuffixTreeNode, sol: list[str], curr_str: str = ''):
        '''
        Find the longest common substring by using a variation of DFS that checks the marks on each node. If a node has all markers it is a common substring so find the longest one.
        - Input:
            - curr (SuffixTreeNode): The current tree node.
            - sol (list[str]): The current solution state.
            - curr_str (str, optional): The current string formed when diving down the tree. Defaults to ''.
        - Time Complexity: O(s), where s is the sum of the lengths of strings inside the suffix tree.
        - Aux space complexity: O(s).
        '''
        for i in curr.children:
            child = self.nodes[i]
            self._longest_common_substring_aux(child, sol, curr_str + child.string)
            if all(child.marks):  # check if there is a common substring
                new_str = curr_str + child.string  # get the new common subtring
                if len(new_str) > len(sol[0]):  # update solution if this new common substring is the longer than the currently found one
                    sol[0] = new_str


def get_whole_percentage(decimal: float) -> int:
    '''
    Alternative to the python round function, used to convert a float into a percentage.
    - Input:
        - decimal (float): The decimal to convert.
    - Returns (int): The percentage rounded to the nearest whole number.
    - Time Complexity: O(1).
    - Aux space complexity: O(1).
    '''
    raw_pct = decimal * 100
    if raw_pct % 1 < 0.5:
        return int(raw_pct)
    return int(raw_pct) + 1


def compare_subs(submission1: str, submission2: str) -> list[str | int]:
    '''
    Compare two strings and determine thier similiarity.
    - Input:
        - submission1 (str): The first string.
        - submission2 (str): The second string.
    - Returns (list[str | int]): A list of three elements:
        - The longest common substring
        - The rounded percentage of submission1 that is the longest common substring
        - The rounded percentage of submission2 that is the longest common substring
    - Time Complexity: O(N+M), where N is the length of submission1 and M is the length of submission2.
    - Aux space complexity: O(N+M).
    '''
    if not submission1 or not submission2:  # if a string is empty
        return ['', 0, 0]
    tree = SuffixTree(submission1, submission2)  # create the tree O((N+M)^2)
    lcs = tree.longest_common_substring()  # get the lcs O(N+M)
    s1_perc = get_whole_percentage(len(lcs) / len(submission1))  # get the lcs percentage of submission1
    s2_perc = get_whole_percentage(len(lcs) / len(submission2))  # get the lcs percentage of submission1
    return [lcs, s1_perc, s2_perc]


def main():
    print(allocate([[3, 1, 0, 0, 1], [1, 2, 2, 2, 1]]))


if __name__ == '__main__':
    main()
