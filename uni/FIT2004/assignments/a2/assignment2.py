# assignment2.py
# Date: 01-09-2022
# Author: Samir Gupta 
from math import inf, isinf
import heapq
from typing import cast

ROAD = tuple[int, int, int]
CAFE = tuple[int, int]
DOWNHILL_ROUTE = tuple[int, int, int]
ADJACENCY_LIST = list[list[tuple[int, int]]]

class Location:
    def __init__(self, id: int, wait_time: int|float = inf):
        """
        Initialise a location.
        - Input:
                - id (int): The id of the location.
                - wait_time (int | float, optional): The wait time for coffee at this location. Defaults to inf.
        - Time Complexity: O(1).
        - Aux space complexity: O(1).
        """
        self.id = id
        self.roads: list[tuple[int, int]] = []
        self.wait_time = wait_time
        
    def __repr__(self) -> str:
        return f'{self.id}({self.wait_time})\n' + ''.join([f' -> {end_id} : {travel_time}\n' for end_id, travel_time in self.roads])

class RoadGraph:
    def __init__(self, roads: list[ROAD], cafes: list[CAFE]):
        """
        Initialise the Road Graph adjacency list.
        - Input:
                - roads (list[tuple[int, int, int]]): A list of roads in the form (u, v, w), where u is the starting location id, v is the finishing location id and w is the amount of time to get from u to v.
                - cafes (list[tuple[int, int]]): A list of cafes in the form (i, j), where i the location id of the cafe and j is the cafe's waiting time.
        - Time Complexity: O(V+E), where V is the amount of locations in the graph, and E is the amount of roads.
        - Aux space complexity: O(V+E).
        """
        if not roads:
            self.locations = 0
        else:
            max_location = max(roads, key=lambda road: max(road[0],road[1])) # O(E), get total amount of locations
            self.locations = max(max_location[0], max_location[1]) + 1 # O(1)
        self.adj_list: list[Location] = [Location(i) for i in range(self.locations)] # O(V), initialise adjacency list
        
        for start, end, travel_time in roads: # O(E), fill adjacency list
            self.adj_list[start].roads.append((end, travel_time)) # O(1)
            
        for id, wait_time in cafes: # O(V), add cafes
            self.adj_list[id].wait_time = wait_time # O(1)
            
    def __repr__(self) -> str: return '\n'.join([str(location) for location in self.adj_list])
    def __getitem__(self, index: int) -> Location: return self.adj_list[index]
    
    def routing(self, start: int, end: int) -> list[int] | None: 
        """
        Find the minimum route from start to end that contains coffee.
        - Input:
                - start (int): The start of the route.
                - end (int): The end of the route.
        - Returns (list[int] | None): List of location id's in order of when they are travelled or None if no route exists. 
        - Time Complexity: O(ElogV) where E is the amount of roads in this road graph and V is the amount of locations.
        This complexity comes from the modified_dijkstra function, since it trumps all other O(V) operations in this function the total cost remains as O(ElogV).
        - Aux space complexity: O(V+E).
        """
        if not self.adj_list:
            return None
        parent, loop, coffee = self.__modified_dijkstra(start=start) # O(ElogV)
        path: list[int] = [end] # O(1)
        found_coffee = self.__coffee_path_traceback(end, start, path, coffee, parent) # # O(V) traceback our path
            
        if not found_coffee: # if we've got to our location but not found coffee yet
            new_current = min(enumerate(loop), key=lambda a: a[1])[0] # O(V) find the id of the minimum loop that contains coffee
            
            if isinf(loop[new_current]):
                return None # if the minimum was infinite there are no loops that contain coffee and start therefore no answer
            
            path.append(new_current) # otherwise add the start of the loop
            self.__coffee_path_traceback(new_current, start, path, coffee, parent) # O(V) traceback loop
            
        return path[::-1] # O(V)
    
    def __modified_dijkstra(self, /, *, start: int = 0) -> tuple[list[int], list[int|float], list[int|float]]:  
        """
        A modified version of Dijkstra's algorithm to find the single sourced shortest path to multiple targets whilst taking into account the coffee wait time.
        - Input:
                - roadGraph (RoadGraph): The adjacency list representation of the graph that describes the roads.
                - start (int, optional): The starting location id. Defaults to 0.
        - Returns (tuple[list[int], list[int|float], list[int|float]]):
            - parent : parent[i] is the next location's id when travelling from i to start.
            - loop : loop[i] stores the time taken to loop back to the start with a coffee stop from i.
            - coffee: coffee[i] stores the minimum wait time when travelling to i from start.
        - Time Complexity: O(ElogV) where E is the amount of roads in the road graph, and V is the amount of locations. 
        This is because pushing an element on the heap is in O(logV) and we do this O(E) times.
        - Aux space complexity: O(V+E) as all created lists are of in O(V) and the priority queue length can be at most O(V+E).
        """
        total, loop, coffee, parent = [], [], [], [] # O(1)
        for _ in range(self.locations): # O(V)
            total.append(inf) # O(1), total[i] stores the minimum total time between the start and i
            loop.append(inf) # O(1), loop[i] stores the time taken to loop back to the start from i (contains a coffee stop)
            coffee.append(inf) # O(1), coffee[i] stores the minimum wait time when travelling to i from start
            parent.append(start) # O(1), parent[i] stores the next location's id from i
        
        coffee[start] = self[start].wait_time # O(1)
        total[start] = 0 if isinf(coffee[start]) else coffee[start] # O(1), if the start is a cafe the minimum time is the wait time at the cafe, otherwise set to 0 to make sure queue starts here (this 0 will be overridden due to the wait time being infinite)
        
        priority_queue: list = [(time, i) for i, time in enumerate(total)] # O(V)
        heapq.heapify(priority_queue) # O(V)
        
        while len(priority_queue): # O(ElogV)
            current = heapq.heappop(priority_queue)[1] # O(1)
            for adj, travel_time in self[current].roads:
                new_time = travel_time + total[current] # O(1) get the new total travel time
                if not isinf(coffee[current]): # if the travel time has a coffee stop included, subtract it off
                    new_time -= coffee[current] # O(1)
                wait_time = min(coffee[current], self[adj].wait_time) # O(1), find the optimal coffee wait time
                new_total_time = wait_time + new_time # O(1), add the wait time to the total time
                if new_total_time < total[adj]: # if this new total time is less than the one previously stored
                    heapq.heappush(priority_queue, (new_total_time, adj)) # O(logV), add edge to queue
                    total[adj] = new_total_time # O(1), update total time
                    coffee[adj] = wait_time # O(1), update the coffee wait time
                    parent[adj] = current # O(1), update the parent
                else: # otherwise make sure total_time is updated with the minimum travel distance (not taking into account coffee wait time)
                    total[adj] = min(total[current] + travel_time, total[adj]) # O(1)
                    
                if adj == start and not isinf(coffee[current]): # if adj forms a loop
                    loop[current] = total[current] # O(1), add so that we know that we can loop after this location
        
        return parent, loop, coffee
        
    def __coffee_path_traceback(self, current: int, start: int, path: list[int], coffee: list[int|float], parent: list[int]) -> bool:
        """
        Traces back a path in place while taking into consideration if coffee was found along the path.
        - Input:
                - current (int): The current location in the path.
                - start (int): The starting location of the path.
                - path (list[int]): List of locations in the path in reverse order.
                - coffee (list[int | float]): List where coffee[i] represents the minimum coffee wait time from start to i (or inf if no cafes).
                - parent (list[int]): List where parent[i] is the next step along the path from i (in reverse order).
        - Returns (bool): Whether coffee was found on the path or not. 
        - Time Complexity: O(V) where V is the amount of vertices in this road graph.
        - Aux space complexity: O(1).
        """
        if current == start:
            if not isinf(coffee[current]):
                return True
        found_coffee = False
        while current != start: # O(V) as len(path) is in O(V)
            if not isinf(coffee[current]): # if coffee is found
                found_coffee = True
            u = parent[current] # O(1)
            path.append(u) # O(1)
            current = u # O(1)
        return found_coffee


def optimalRoute(downhillScores: list[DOWNHILL_ROUTE], start: int, finish: int) -> list[int] | None:
    """
    Finds the optimal route to maximise tournament score with set downhill routes from start to finish.
    - Input:
            - downhillScores (list[DOWNHILL_ROUTE]): The list of downhill routes with their score.
            - start (int): The starting intersection point.
            - end (int): The ending intersection point.
    - Returns (list[int] | None): A list of integers that describe the path for the optimal route or None if no such path exists. 
    - Time Complexity: O(D) where D is the amount of downhill routes, this is assuming that O(D+P), where P is the amount of intersection points, simplifies to O(D) as for each P there is at least one D that starts or finishes at it (D>=P-1).
    - Aux space complexity: O(D).
    """
    max_point = max(downhillScores, key=lambda a: max(a[0], a[1])) # O(D)
    intersection_points = max(max_point[0], max_point[1]) + 1 # O(1)
    graph: list[list[tuple[int, int]]] = [[] for _ in range(intersection_points)] # O(D)
    for top, bottom, score in downhillScores: # O(D), create adjacency list in opposite order (graph[i] stores i's parents)
        graph[bottom].append((top, score)) # O(1)
    
    memo: list[int|float|None] = [None for _ in range(len(graph))] # O(D) create the memo list
    path: list[int] = [] # O(1) initialise path
    if start == finish: # if we are going from one location to the same location there is only one way
        return [start] # O(1)
    
    def optimalRoute_aux(current: int, graph: ADJACENCY_LIST) -> int|float: # aux function
        """
        Auxillary function for optimalRoute that does all the work to find the maximum score path.
        - Input:
                - current (int): The current location id.
                - graph (ADJACENCY_LIST): The graph's adjacency list, where graph[i] contains the parents of i and the score to get to i from that parent.
        - Returns (int|float): Largest score value to get to current in the graph. 
        - Time Complexity: O(D) where is D is the amount of edges in the graph, as with the memo array it ensures that each edge is only visited once and there are only constant time operations per edge.
        - Aux space complexity: O(D).
        """
        if current == start: # if we have hit the start, return 0 for the score
            return 0 # O(1)
        
        if len(graph[current]) == 0: # if we have hit the top of the hill/mountain without hitting start then this path is not valid so return -inf
            return -inf # O(1)
        
        if memo[current] is None: # if we haven't stored this value yet
            max_i = -1 # initialise location 
            max_score = -inf # initialise a max score
            for parent, weight in graph[current]: # check each parent to find the largest score, O(D) in total
                score = optimalRoute_aux(parent, graph) + weight
                if score > max_score:
                    max_i = parent
                    max_score = score
            if max_i != -1: # if we didnt find a valid path don't add the index
                if path: 
                    if path[-1] != max_i: # to ensure no duplicate locations
                        path.append(max_i)
                else:
                    path.append(max_i)
            memo[current] = max_score # store the value in the memo
            return max_score
        
        return cast(int, memo[current]) # if value is stored return it
    
    optimalRoute_aux(finish, graph) # O(D) run aux function
    if not path: # if no maximal path is found (no path from start to finish) return None
        return None
    path.append(finish) # add the end to the path
    return path # otherwise we have a maximum path so return it 
    

def main():
    downhillScores = [(0, 6, -500), (1, 4, 100), (1, 2, 300), (6, 3, -100), (6, 1, 200), (3, 4, 400), (3, 1, 400), (5, 6, 700), (5, 1, 1000), (4, 2, 100)]
    start = 5
    finish = 2
    print(optimalRoute(downhillScores, start, finish))

if __name__ == '__main__': main()