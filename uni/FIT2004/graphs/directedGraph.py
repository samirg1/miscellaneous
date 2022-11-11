# directedGraph.py
# Date: 23-08-2022
# Author: Samir Gupta

class DirectedGraph:
    def __init__(self, n: int, /):
        if n < 0:
            raise ValueError(f'Invalid amount of vertexes "{n}"')
        self.vertices = n
        self.edges = 0
        self.matrix = [[0]*n for _ in range(n)]
        
    def __repr__(self) -> str:
        return str(self.matrix)
    
    def add_edge(self, fro: int, to: int, /, *, weight: int) -> None:
        if fro == to:
            raise ValueError(f'Vertexes cannot be the same, got "{fro}" and "{to}"')
        if fro < 0 or fro > self.vertices-1:
            raise ValueError(f"Origin vertex out of range, got '{fro}'")
        if to < 0 or to > self.vertices-1:
            raise ValueError(f"End vertex out of range, got '{to}'")
        self[fro][to] = weight
        self.edges += 1
        
    def __getitem__(self, n:int) -> list: 
        return self.matrix[n]



def main():
    x = DirectedGraph(3)

    x.add_edge(1, 0, weight=10)
    x.add_edge(1, 2, weight=15)
    
    print(x)
    print(x[1])

if __name__ == '__main__':
    main()