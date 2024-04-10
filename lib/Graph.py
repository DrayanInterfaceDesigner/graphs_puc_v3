

class Graph:
    def __init__(self, directed:bool, weighted:bool, representation:str) -> None:
        self.vertices:list = [{0: 'A'}, {1: 'B'}, {2: 'C'}, {3: 'D'}, {4: 'E'}, {5: 'F'}, {6: 'G'}, {7: 'H'}, {8: 'I'}, {9: 'J'}]
        self.connections:list = []
        self.directed:bool = directed
        self.weighted:bool = weighted
        self.representation:str = representation
    
    def add_vertice(self, name:str) -> None:
        if name not in self.vertices:
            self.vertices.append(name)
    
    def add_edge(self, parent:str, child:str, weight:int=1) -> None:
        self.connections.append({'parent': parent, 'child': child, 'weight': weight})
    
    def remove_vertice(self, name:str) -> None:
        pass
    
    def remove_edge(self, vertice:str) -> None:
        pass

    def get_adjacent(self, vertice:str) -> list:
        adjacent:list = []
        for connection in self.connections:
            if connection['parent'] == vertice:
                adjacent.append(connection['child'])
        return adjacent
    
    def out_degree(self, vertice:str) -> int:
        degree:int = 0
        for connection in self.connections:
            if connection['parent'] == vertice:
                degree += 1
        return degree

    def in_degree(self, vertice:str) -> int:
        degree:int = 0
        for connection in self.connections:
            if connection['child'] == vertice:
                degree += 1
        return degree
    
    def degree(self, vertice:str) -> int:
        if self.directed:
            return self.in_degree(vertice) + self.out_degree(vertice)
        else:
            return self.in_degree(vertice)
    
    def is_adjacent(self, vertice1:str, vertice2:str) -> bool:
        for connection in self.connections:
            if connection['parent'] == vertice1 and connection['child'] == vertice2:
                return True
        return False
    
    def dijkstra(self, start:str, end:str) -> int:
        pass

    def warshall(self) -> list:
        pass
    
    def __str__(self) -> str:
        return f"Graph: {self.vertices} {self.connections}"

    def __repr__(self) -> str:
        return f"Graph: {self.vertices} {self.connections}"

