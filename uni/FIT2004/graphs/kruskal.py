from typing import Generic, TypeVar

T = TypeVar('T')

class DisjointSet(Generic[T]):
    def __init__(self, elements: list[T]) -> None:
        self.parent = {e: e for e in elements}
        
    def find(self, vertex: T) -> T:
        while self.parent[vertex] != vertex:
            vertex, self.parent[vertex] = self.parent[vertex], self.parent[self.parent[vertex]]
        return vertex
        
    def union(self, set1: T, set2: T) -> None:
        if set1 == set2:
            return
        self.parent[self.find(set2)] = self.find(set1)
        
    def in_same_set(self, set1: T, set2: T) -> bool:
        return self.find(set1) == self.find(set2)
        
    def __repr__(self) -> str:
        sets: dict[T, list[T]] = {v: [] for v in self.parent}
        for key, val in self.parent.items():
            sets[self.find(val)].append(key)
        out = ''
        for key, lst in sets.items():
            out += f'{key}: {lst}\n'
        return out
    
def kruskals(graph: list[list[int]]) -> list[list[int]]:
    kruskal: list[list[int]] = [[0 for _ in row] for row in graph]
    ds = DisjointSet([i for i in range(len(graph))])
    edges: list[tuple[int, int, int]] = sorted([
        (i, j, graph[i][j]) for i in range(len(graph)) for j in range(len(graph)) if graph[i][j]
    ], key=lambda edge: edge[2])
    
    for start, end, weight in edges:
        if not ds.in_same_set(start, end):
            kruskal[start][end] = weight
            ds.union(start, end)        
    return kruskal
    
def main(): 
    graph = [
        [0, 10, 5, 0, 0],
        [10, 0, 3, 1, 0],
        [5,  3, 0, 9, 2],
        [0,  1, 9, 0, 4],
        [0,  0, 2, 4, 0]
    ]
    print(kruskals(graph))

if __name__ == '__main__':
    main()