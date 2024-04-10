

class Graph:
    def __init__(self, directed:bool, weighted:bool, representation:str) -> None:
        self.vertices:list = []
        self.connections:list = []
        self.directed:bool = directed
        self.weighted:bool = weighted
        self.representation:str = representation
    

    def find_vertice(self, name:str) -> dict:
        for vertice in self.vertices:
            if list(vertice.values())[0] == name:
                return vertice
        return None

    def add_vertice(self, name:str) -> None:
        if not self.find_vertice(name):
            self.vertices.append({len(self.vertices): name})
    
    def add_edge(self, parent:str, child:str, weight:int=1) -> None:
        self.connections.append({'parent': parent, 'child': child, 'weight': weight})
    
    def remove_vertice(self, name:str ) -> None:
        to_remove:list = []
        for connection in self.connections:
            if connection['parent'] == name or connection['child'] == name:
                to_remove.append(connection)
        
        for connection in to_remove:
            self.connections.remove(connection)
        
        self.vertices = [vertice for vertice in self.vertices if list(vertice.values())[0] != name]
    
    def remove_edge(self, vertice_a:str, vertice_b:str) -> None:
        to_remove:list = []

        for connection in self.connections:
            if connection['parent'] == vertice_a and connection['child'] == vertice_b:
                to_remove.append(connection)
            elif connection['parent'] == vertice_b and connection['child'] == vertice_a:
                to_remove.append(connection)
            
        for connection in to_remove:
            self.connections.remove(connection)
        

    def get_adjacent(self, vertice:str) -> list:
        adjacent:list = []
        for connection in self.connections:
            if connection['parent'] == vertice:
                adjacent.append(connection['child'])
            elif connection['child'] == vertice:
                adjacent.append(connection['parent'])
        
        adjacent = list(set(adjacent))
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
        return f"Graph: v: {self.vertices} c: {self.connections}"

    def __repr__(self) -> str:
        return f"Graph: v: {self.vertices} c: {self.connections}"

