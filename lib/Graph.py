

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
    
    def find_edge(self, vertice_a:str, vertice_b:str) -> bool:
        for connection in self.connections:
            if ((connection['parent'] == vertice_a and connection['child'] == vertice_b) or 
                (connection['parent'] == vertice_b and connection['child'] == vertice_a)):
                return True
            else: 
                return False
                

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
        

    def get_adjacencies(self, vertice:str) -> list:
        adjacent:list = []
        for connection in self.connections:
            if connection['parent'] == vertice:
                adjacent.append(connection['child'])
            elif connection['child'] == vertice:
                adjacent.append(connection['parent'])
        
        adjacent = list(set(adjacent))
        return adjacent
    

    def get_weight(self, vertice_a:str, vertice_b:str) -> (int|float|None):
        if not self.weighted:
            return 1
        elif not self.find_edge(vertice_a, vertice_b):
            return None
        else:
            for connection in self.connections:
                if connection['parent'] == vertice_a and connection['child'] == vertice_b:
                    return connection['weight']
                
    def set_weight(self, vertice_a:str, vertice_b:str, weight:int|float) -> None:
        if self.weighted:
            if not self.find_edge(vertice_a, vertice_b):
                self.add_edge(vertice_a, vertice_b, weight)
            else:
                for connection in self.connections:
                    if connection['parent'] == vertice_a and connection['child'] == vertice_b:
                        connection['weight'] = weight
        else:
            if not self.find_edge(vertice_a, vertice_b):
                self.add_edge(vertice_a, vertice_b)


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
    

    def dijkstra(self, start:str, end:str) -> int:
        pass

    def warshall(self) -> list:
        pass
    
    def __str__(self) -> str:
        return f"Graph: v: {self.vertices} c: {self.connections}"

    def __repr__(self) -> str:
        return f"Graph: v: {self.vertices} c: {self.connections}"

