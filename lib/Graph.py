import time
# import numpy as np

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
        return False
                
    def add_vertice(self, name:str) -> None:
        if not self.find_vertice(name):
            self.vertices.append({len(self.vertices): name})
    
<<<<<<< Updated upstream
    def add_edge(self, parent:str, child:str, weight:int=1) -> None:
        self.connections.append({'parent': parent, 'child': child, 'weight': weight})
=======
    def add_edge(self, parent:str, child:str, weight:int|float=1) -> None:
        w:int|float = 1 if not self.weighted else weight
        self.connections.append({'parent': parent, 'child': child, 'weight': w})
        self.connections.append({'parent': child, 'child': parent, 'weight': w})
>>>>>>> Stashed changes
    
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


    def depth_search(self, start:str, end:str) -> int:
        if not self.find_vertice(start) or not self.find_vertice(end):
            return 0
        
        start_time = time.perf_counter()

        stack = []
        visited = []
        stack.append(start)

        while len(stack) > 0:
            vertice = stack.pop(-1)
            if vertice not in visited:
                visited.append(vertice)
            for adjacency in sorted(self.get_adjacencies(vertice)):
                if adjacency not in visited:
                    stack.append(adjacency)
            if vertice == end:
                break

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return visited, total_time

    def width_search(self, start:str, end:str) -> int:
        if not self.find_vertice(start) or not self.find_vertice(end):
            return 0
        
        start_time = time.perf_counter()

        queue = []
        visited = []
        queue.append(start)

        while len(queue) > 0:
            vertice = queue.pop(0)
            if vertice not in visited:
                visited.append(vertice)
            for adjacency in sorted(self.get_adjacencies(vertice)):
                if adjacency not in visited:
                    queue.append(adjacency)
            if vertice == end:
                break

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return visited, total_time
    
<<<<<<< Updated upstream
=======
    # dijkstra helper, determines min cost vertice
    def extract_min(self, q, costs):
        min_cost_vertice = None
        min_weight = +1e10
        for vertice in q:
            if costs[vertice] <= min_weight:
                min_weight = costs[vertice]
                min_cost_vertice = vertice
        return min_cost_vertice

>>>>>>> Stashed changes
    def dijkstra(self, start:str, end:str) -> int:
        if not self.find_vertice(start) or not self.find_vertice(end):
            return 0
        
        start_time = time.perf_counter()

        pi = {}
        costs = {}
        q = []
        path = []
        total_cost = 1e10
        named_vertices = [list(x.values())[0] for x in self.vertices]

        for vertice in named_vertices:
            costs[vertice] = +1e10 # infinite
            pi[vertice] = None
        costs[start] = 0.0
        for vertice in named_vertices:
            q.append(vertice)
        while len(q) > 0:
            vertice = self.extract_min(q, costs)
            if vertice is None:
                break
            q.remove(vertice)
            for adjacency in self.get_adjacencies(vertice):
                new_cost = costs[vertice] + self.get_weight(vertice, adjacency)
                if new_cost < costs[adjacency]:
                    costs[adjacency] = new_cost
                    pi[adjacency] = vertice
        if pi[end] != None:
            total_cost = costs[end]
            vertice = end
            while vertice != None:
                path.insert(0, vertice)
                vertice = pi[vertice]

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return path, total_cost, total_time


    def warshall(self) -> list:
        pass
    
    def __str__(self) -> str:
        return f"Graph: v: {self.vertices} c: {self.connections}"

    def __repr__(self) -> str:
        return f"Graph: v: {self.vertices} c: {self.connections}"

