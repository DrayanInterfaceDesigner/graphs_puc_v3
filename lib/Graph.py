import time
import matplotlib.pyplot as plt

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
    
    def add_edge(self, parent:str, child:str, weight:int|float=1) -> None:
        w:int|float = 1 if not self.weighted else weight
        self.connections.append({'parent': parent, 'child': child, 'weight': w})
        self.connections.append({'parent': child, 'child': parent, 'weight': w})
    
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
    
    # dijkstra helper, determines min cost vertice
    def extract_min(self, q, costs):
        min_cost_vertice = None
        min_weight = +1e10
        for vertice in q:
            if costs[vertice] <= min_weight:
                min_weight = costs[vertice]
                min_cost_vertice = vertice
        return min_cost_vertice

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


    def is_connected(self):
        # TODO: fazer funsionar
        return True

    def prim(self):
        if self.is_connected():
            predecessors = {}
            weights = {}
            named_vertices = [list(x.values())[0] for x in self.vertices]

            for vertice in named_vertices:
                predecessors[vertice] = None
                weights[vertice] = 1e10
            q = [x for x in named_vertices]
            while len(q) > 0:
                u = self.extract_min(q, weights)
                q.remove(u)

                for adjacency in self.get_adjacencies(u):
                    weight = self.get_weight(u, adjacency)
                    if adjacency in q and weight < weights[adjacency]:
                        predecessors[adjacency] = u
                        weights[adjacency] = weight

            Prim_Graph = Graph(False, True, self.representation)

            for vertice in named_vertices:
                Prim_Graph.add_vertice(vertice)

            cost = 0
            for start_vertice in predecessors.keys():
                end_vertice = predecessors[start_vertice]
                if end_vertice is not None:
                    Prim_Graph.add_edge(start_vertice, end_vertice, weights[start_vertice])
                    cost += weights[start_vertice]

            return Prim_Graph, cost


    def warshall(self) -> list:
        matrix = self.generate_matrix()
        for k in range(len(matrix)):
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    matrix[i][j] = matrix[i][j] or (matrix[i][k] and matrix[k][j])
        
        return matrix


    def generate_nodes_string(self) -> str:
        vertices:list = []
        vertices_str:str = "Nodes: \n"

        for vertice in self.vertices:
            vertices.append(f"{list(vertice.values())[0]} ({list(vertice.keys())[0]})")
        
        vertices_str += ', '.join(vertices)
        return vertices_str


    def generate_matrix(self) -> list:
        matrix:list = []

        for vertice in self.vertices:

            slots:list = [0] * len(self.vertices)
            va:str = list(vertice.values())[0]
            
            for vb in self.vertices:
                _b:str = list(vb.values())[0]
                adjacencies:list = self.get_adjacencies(_b)
                if va in adjacencies:
                    slots[self.vertices.index(vb)] = 1
                    
            matrix.append(slots)
        
        return matrix

    def to_string_matrix(self) -> str:
        connections_str:str = "Edges: \n"
        final_string:str = ""
        binary_adjacencies:list = []

        list(self.vertices[0].values())[0]

        for vertice in self.vertices:

            slots:list = ['0'] * len(self.vertices)
            va:str = list(vertice.values())[0]
            
            for vb in self.vertices:
                _b:str = list(vb.values())[0]
                adjacencies:list = self.get_adjacencies(_b)
                if va in adjacencies:
                    slots[self.vertices.index(vb)] = '1'
                    
            text:str = f"{va} ({list(vertice.keys())[0]}): {' '.join(slots)}"
            binary_adjacencies.append(text)
        
        final_string += "\n" + self.generate_nodes_string() + "\n"
        final_string += "\n" + connections_str
        final_string += '\n'.join(binary_adjacencies)

        return final_string

    def to_string_list(self) -> str:

        connections_str:str = "Edges: \n"
        final_string:str = ""
        adjacencies:list = [(v, self.get_adjacencies(list(v.values())[0])) for v in self.vertices]

        for adjacency in adjacencies:
            parent:str = list(adjacency[0].values())[0]
            parent_index:str = list(adjacency[0].keys())[0]
            connections_str+= f"{parent} ({parent_index}): {', '.join(adjacency[1])}\n"
                
        final_string += "\n" + self.generate_nodes_string() + "\n"
        final_string += "\n" + connections_str

        return final_string
    

    def to_pajek(self):

        final_string:str = ""

        configuration:str = ""
        configuration+= f"% directed={self.directed}\n"
        configuration+= f"% weighted={self.weighted}\n"
        repr_key:str = "adjacency_matrix" if self.representation == "MATRIZ" else "edge_list"
        configuration+= f"% representation={repr_key}\n"

        vertices:str = ""
        vertices+= f"*Vertices\n"
        vertices+= '\n'.join([' '.join([str(list(v.keys())[0]), list(v.values())[0]]) for v in self.vertices])

        edges:str = ""
        edges+= f"*arcs\n"
        edges+= '\n'.join([' '.join([str(v['parent']), str(v['child']), str(v['weight']) if self.weighted else ''])  for v in self.connections])

        final_string+= configuration
        final_string+= vertices
        final_string+="\n\n"
        final_string+=edges

        return final_string



    def __str__(self) -> str:
        if self.representation == 'MATRIZ':
            return self.to_string_matrix()
        return self.to_string_list()

    def __repr__(self) -> str:
        return f"Graph: v: {self.vertices} c: {self.connections}"

