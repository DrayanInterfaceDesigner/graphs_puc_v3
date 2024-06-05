import time
import matplotlib.pyplot as plt


class Graph:
    """Graph manipulation and representation."""
    def __init__(self, directed: bool, weighted: bool, representation: str):
        self.directed:bool = directed
        self.weighted:bool = weighted
        self.representation:str = representation

        if self.representation == 'LIST':
            self.aList = {}
            # {'A': {'C': 1, 'B': 1}, 'B': {'A': 1}, 'C': {'A': 1}}
        elif self.representation == 'MATRIX':
            self.aMatrix = []
            # [[None, 1, 1], [1, None, None], [1, None, None]]
            self.nameDict = {}
            # {'A': 0, 'B': 1, 'C': 2}
        

    def find_vertice(self, name:str) -> bool:
        """Finds a vertice by name."""
        if self.representation == "LIST":
            if name in self.aList:
                return True   
        elif self.representation == "MATRIX":
            if name in self.nameDict:
                return True
        return False

    def find_edge(self, parent:str, child:str) -> bool:
        """Finds an edge in the graph using the names of the vertices it connects."""
        if not self.find_vertice(parent) or not self.find_vertice(child):
            return False
        elif self.representation == "LIST":
            if child in self.aList[parent].keys():
                return True
        elif self.representation == "MATRIX":
            if self.aMatrix[self.nameDict[parent]][self.nameDict[child]]:
                return True
        return False

    def add_vertice(self, name:str) -> None:
        """Adds a vertice to the graph."""
        if not self.find_vertice(name):
            if self.representation == "LIST":
                self.aList.update({name : {}})
            elif self.representation == "MATRIX":
                self.nameDict.update({name : len(self.nameDict)})
                arr = []
                for i in range(len(self.nameDict)):
                    arr.append(None)
                for array in self.aMatrix:
                    array.append(None)
                self.aMatrix.append(arr)

    def add_edge(self, parent:str, child:str, weight:int|float=1) -> None:
        """Adds an edge to the graph. Takes both connected vertices as parameters."""
        if self.find_vertice(parent) and self.find_vertice(child):
            if self.representation == "LIST":
                if child not in self.aList[parent].keys():
                    self.aList[parent].update({child : weight})
                    if not self.directed:
                        self.aList[child].update({parent : weight})
            elif self.representation == "MATRIX":
                if not self.aMatrix[self.nameDict[parent]][self.nameDict[child]]:
                    self.aMatrix[self.nameDict[parent]][self.nameDict[child]] = weight
                    if not self.directed:
                        self.aMatrix[self.nameDict[child]][self.nameDict[parent]] = weight

    def remove_vertice(self, name:str) -> None:
        """Removes a vertice from the graph, as well as any edges that connect to it."""
        if self.find_vertice(name):
            if self.representation == "LIST":
                del self.aList[name]
                for key in self.aList:
                    if name in self.aList[key]:
                        del self.aList[key][name]
            elif self.representation == "MATRIX":
                del self.aMatrix[self.nameDict[name]]
                for i in self.aMatrix:
                    for j in range(len(i)):
                        if j == self.nameDict[name]:
                            del i[j]
                for i in self.nameDict:
                    if self.nameDict[i] > self.nameDict[name]:
                        self.nameDict[i] -= 1
                del self.nameDict[name]

    def remove_edge(self, parent:str, child:str):
        """Removes an edge from the graph."""
        if self.find_vertice(parent) and self.find_vertice(child):
            if self.representation == "LIST":
                if child in self.aList[parent].keys():
                    del self.aList[parent][child]
                    if not self.directed:
                        del self.vertex_list[child][parent]
            elif self.representation == "MATRIX":
                if self.aMatrix[self.nameDict[parent]][self.nameDict[child]]:
                    self.aMatrix[self.nameDict[parent]][self.nameDict[child]] = None
                    if not self.directed:
                        self.aMatrix[self.nameDict[child]][self.nameDict[parent]] = None


    def get_adjacencies(self, vertice:str) -> list:
        """Returns a list containing all adjacencies of the vertice."""
        if self.find_vertice(vertice):
            adjacencies = {}
            if self.representation == "LIST":
                for i in self.aList[vertice]:
                    adjacencies[i] = self.aList[vertice][i]
                return adjacencies
            elif self.representation == "MATRIX":
                for i in range(len(self.aMatrix[self.nameDict[vertice]])):
                    # print(self.aMatrix[self.nameDict[vertice]][i])
                    if self.aMatrix[self.nameDict[vertice]][i] != None:
                        for key, value in self.nameDict.items():
                            if value == i:
                                adjacencies[key] = self.nameDict[key]
                return adjacencies


    def get_weight(self, parent:str, child:str) -> (int|float|None):
        """Returns the weight of an edge. Takes both connected vertices as parameters."""
        if self.find_edge(parent, child):
            if not self.weighted:
                return 1
            elif self.representation == "LIST":
                return self.aList[parent][child]
            elif self.representation == "MATRIX":
                return self.aMatrix[self.nameDict[parent]][self.nameDict[child]]

    def set_weight(self, parent:str, child:str, weight:int|float) -> None:
        """Updates an edge's weight. If no such edge exists, creates it."""
        if not self.find_edge(parent, child):
            self.add_edge(parent, child, weight)
        elif self.representation == "LIST":
            self.aList[parent].update({child : weight})
            if not self.directed:
                self.aList[child].update({parent : weight})
        elif self.representation == "MATRIX":
            self.aMatrix[self.nameDict[parent]][self.nameDict[child]] = weight
            if not self.directed:
                self.aMatrix[self.nameDict[child]][self.nameDict[parent]] = weight


    def out_degree(self, name:str) -> int:
        """Returns a vertice's outdegree."""
        if self.find_vertice(name):
            if self.representation == "LIST":
                return len(self.aList[name])
            elif self.representation == "MATRIX":
                degree:int = 0
                for i in self.aMatrix[self.nameDict[name]]:
                    if i: 
                        degree += 1
                return degree        

    def in_degree(self, name:str) -> int:
        """Returns a vertice's indegree."""
        if self.find_vertice(name):
            degree:int = 0
            if self.representation == "LIST":
                for vertice in self.aList:
                    if vertice != name:
                        for i in self.aList[vertice]:
                            if i == name:
                                degree += 1
                return degree
            elif self.representation == "MATRIX":
                for i in self.aMatrix:
                    for j in range(len(i)):
                        if j == self.nameDict[name] and i[j]:
                            degree += 1
                return degree

    def degree(self, name:str) -> int:
        """Returns a vertice's degree."""
        if self.find_vertice(name):
            if self.directed:
                return self.in_degree(name) + self.out_degree(name)
            else:
                return self.out_degree(name)
            
    
    def depth_search(self, start:str, end:str) -> int:
        """Finds the shortest path to another vertice using a depth-based search."""
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
            for adjacency in self.get_adjacencies(vertice):
                if adjacency not in visited:
                    stack.append(adjacency)
            if vertice == end:
                break

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return visited, total_time

    def width_search(self, start:str, end:str) -> int:
        """Finds the shortest path to another vertice using a width-based search."""
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
            for adjacency in self.get_adjacencies(vertice):
                if adjacency not in visited:
                    queue.append(adjacency)
            if vertice == end:
                break

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return visited, total_time
    
    def extract_min(self, q, costs):
        """Dijkstra helper, determines min cost vertice"""
        min_cost_vertice = None
        min_weight = +1e10
        for vertice in q:
            if costs[vertice] <= min_weight:
                min_weight = costs[vertice]
                min_cost_vertice = vertice
        return min_cost_vertice

    def dijkstra(self, start:str, end:str, w:bool = False) -> int:
        """Finds the shortest path to another vertice using dijkstra's algorithm."""
        if not self.find_vertice(start) or not self.find_vertice(end):
            return 0
        
        start_time = time.perf_counter()

        pi = {}
        costs = {}
        q = []
        path = []
        total_cost = 1e10
        
        if self.representation == "LIST":
            named_vertices = self.aList
        elif self.representation == "MATRIX":
            named_vertices = self.nameDict

        for vertice in named_vertices:
            costs[vertice] = +1e10 # infinite
            pi[vertice] = None
        costs[start] = 0.0
        for vertice in named_vertices:
            q.append(vertice)
        while len(q) > 0:
            currentVertice = self.extract_min(q, costs)
            if currentVertice is None:
                break
            q.remove(currentVertice)
            for adjacency in self.get_adjacencies(currentVertice):
                # Test
                if not w:
                    new_cost = costs[currentVertice] + self.get_weight(currentVertice, adjacency)
                else:
                    new_cost = costs[currentVertice] + 1
                # End test
                if new_cost < costs[adjacency]:
                    costs[adjacency] = new_cost
                    pi[adjacency] = currentVertice
        if pi[end] != None:
            total_cost = costs[end]
            currentVertice = end
            while currentVertice != None:
                path.insert(0, currentVertice)
                currentVertice = pi[currentVertice]

        end_time = time.perf_counter()
        total_time = end_time - start_time

        return path, total_cost, total_time
    
    def DJ_kstra(self, start:str) -> list:
        """Finds the shortest path to all other vertices using dijkstra's algorithm."""
        if not self.find_vertice(start):
            return 0
        
        if self.representation == "LIST":
            vertices = self.aList
        elif self.representation == "MATRIX":
            vertices = self.nameDict

        distances:dict = {v: float('inf') for v in vertices}
        distances[start] = 0
        visited:dict = {v: [] for v in vertices}
        unvisited = set(vertices)
        all_paths:dict = {}

        start_time = time.perf_counter()

        while unvisited:
            current = min(unvisited, key=lambda v: distances[v])
            unvisited.remove(current)
            for neighbor in self.get_adjacencies(current):
                if neighbor in unvisited:
                    new_distance = distances[current] + self.get_weight(current, neighbor)
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        # visited[neighbor] = visited[current] + [neighbor]
                        visited[neighbor] = [current]
                    elif new_distance == distances[neighbor]:
                        visited[neighbor].append(visited[current] + [neighbor])
        
        for vertice in visited:
            if vertice == start:
                all_paths[vertice] = [start]
            elif distances[vertice] == float('inf'):
                all_paths[vertice] = []
            else:
                paths: list = [[start]]
                while paths:
                    path = paths.pop(0)
                    for v in visited[path[0]]:
                        new_path = [v] + path
                        if v == start:
                            all_paths[vertice] = new_path
                        else:
                            paths.append(new_path)
        
        return all_paths, time.perf_counter() - start_time

    def is_connected(self):
        """Returns whether a graph is connected."""
        warshall = self.warshall()
        matrix = warshall.aMatrix
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == None:
                    return False  
        return True

    def prim(self):
        """Returns a graph's minimum spanning tree using Prim's algorithm."""
        if not self.directed and self.weighted:
            if self.is_connected():
                predecessors = {}
                weights = {}
                q = []
        
                if self.representation == "LIST":
                    vertices = self.aList.keys()
                elif self.representation == "MATRIX":
                    vertices = self.nameDict.keys()

                for i in vertices:
                    q.append(i)
                    predecessors[i] = None
                    weights[i] = 1e10
                while len(q) > 0:
                    u = self.extract_min(q, weights)
                    q.remove(u)
                    for adjacency in self.get_adjacencies(u):
                        weight = self.get_weight(u, adjacency)
                        if adjacency in q and weight < weights[adjacency]:
                            predecessors[adjacency] = u
                            weights[adjacency] = weight
                primGraph = Graph(False, True, self.representation)
                for vertice in vertices:
                    primGraph.add_vertice(vertice)
                cost = 0
                for start_vertice in predecessors.keys():
                    end_vertice = predecessors[start_vertice]
                    if end_vertice is not None:
                        primGraph.add_edge(start_vertice, end_vertice, weights[start_vertice])
                        cost += weights[start_vertice]

                return primGraph, cost

    def eulerian(self):
        """Returns whether a graph is considered eulerian."""
        if self.representation == "MATRIX":
            vertices_list = self.nameDict.keys()
        elif self.representation == "LIST":
            vertices_list = self.aList.keys()
        if self.directed:
            for vertice in vertices_list:
                if self.in_degree(vertice) != self.out_degree(vertice):
                    return False
            if self.is_connected():
                return True
        else:
            if self.is_connected():
                for vertice in vertices_list:
                    if self.degree(vertice) % 2 != 0:
                        return False
                return True
            return False

    def warshall(self):
        """Returns an adjacency matrix representing a graph's transitive closure using Warshall's algorithm.
        
        Creates a new graph if the original graph's representation is "LIST", as it needs a matrix to run.
        """

        if self.representation == "MATRIX":
            wMatrixGraph = Graph(self.directed, self.weighted, "MATRIX")
            for i in self.nameDict.keys():
                wMatrixGraph.add_vertice(i)
            for i in self.nameDict.keys():
                for adjacency in self.get_adjacencies(i).keys():
                    wMatrixGraph.add_edge(i, adjacency, self.aMatrix[self.nameDict[i]][self.nameDict[adjacency]])
            wMatrix = wMatrixGraph.aMatrix.copy()
        elif self.representation == "LIST":
            # Creates a new matrix graph so that warshall can run
            wMatrixGraph = Graph(self.directed, self.weighted, "MATRIX")
            for i in self.aList.keys():
                wMatrixGraph.add_vertice(i)
            for i in self.aList.keys():
                for adjacency in self.aList[i].keys():
                    wMatrixGraph.add_edge(i, adjacency, self.aList[i][adjacency])
            wMatrix = wMatrixGraph.aMatrix.copy()
        # actual warshall
        for k in range(len(wMatrix)):
            for i in range(len(wMatrix)):
                for j in range(len(wMatrix)):
                    wMatrix[i][j] = wMatrix[i][j] or (wMatrix[i][k] and wMatrix[k][j])
        newGraph = Graph(wMatrixGraph.directed, wMatrixGraph.weighted, "MATRIX")
        for i in wMatrixGraph.nameDict.keys():
            newGraph.add_vertice(i)
        names = {}
        for vertice, index in wMatrixGraph.nameDict.items():
            names[str(index)] = vertice
        for i in range(len(wMatrixGraph.aMatrix)):
            for j in range(len(wMatrixGraph.aMatrix)):
                if wMatrix[i][j] != None:
                    newGraph.add_edge(names[str(i)], names[str(j)], wMatrix[i][j])
        return newGraph

    def degree_distribution_histogram(self):
        """Plots a histogram representing the distribution of degrees throughout the graph."""
        degrees = []
        if self.representation == "LIST":
            vertices = list(self.aList.keys())
        elif self.representation == "MATRIX":
            vertices = list(self.nameDict.keys())
        for vertice in vertices:
            degrees.append(self.degree(vertice))

        plt.hist(degrees, bins=range(min(degrees), max(degrees) + 1), alpha=0.7, color='purple', edgecolor='cyan')
        plt.title('Degree Distribution')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.savefig("degree_distribution.png")
        plt.show()
    

    def __str__(self):
        """Defines string representation."""
        index = 0
        a = ""
        b = ""
        finalString = "Nodes: "
        if self.representation == "LIST":
            for i in self.aList.keys():
                a += f"{i}({index}), "
                b += f"{i}({index}): "
                for j in self.aList[i].keys():
                    b += f"{j}, "
                index += 1
                b = b[0:-2] + "\n"
            finalString += a[0:-2]
            finalString += "\nEdges:\n"
            finalString += b
            return finalString
        elif self.representation == "MATRIX":
            for i in self.nameDict.keys():
                a += f"{i}({index}), "
                b += f"{i}({index}): "
                for j in self.aMatrix[self.nameDict[i]]:
                    if j == None:
                        j = 0
                    b += f"{j} "
                index += 1
                b += "\n"
            finalString += a[0:-2]
            finalString += "\nEdges:\n"
            finalString += b
            return str(finalString)
        
    
    def to_pajek(self):
        """Turns the graph into a string to be passed to the parser for pajek persistance."""
        finalString:str = ""

        configuration:str = ""
        configuration += f"% directed={self.directed}\n"
        configuration += f"% weighted={self.weighted}\n"
        configuration += f"% representation={self.representation}\n"
        
        vertices:str = ""
        vertices += f"*Vertices {len(self.aList) if self.representation == 'LIST' else len(self.nameDict)}\n"

        edges:str = ""
        edges += f"*arcs\n"

        if self.representation == "LIST":
            indexes = {vertice: index for index, vertice in enumerate(self.aList.keys())}
            for index, vertice in enumerate(self.aList.keys()):
                vertices += f"{index} {vertice}\n"

            for vertice, adjacencies in self.aList.items():
                verticeIndex = indexes[vertice]
                for adjacency, weight in adjacencies.items():
                    adjacencyIndex = indexes[adjacency]
                    if not self.weighted and weight is not None:
                        edges += f"{verticeIndex} {adjacencyIndex}\n"
                    elif self.weighted and weight is not None:
                        edges += f"{verticeIndex} {adjacencyIndex} {weight}\n"
        elif self.representation == "MATRIX":
            for vertice, index in self.nameDict.items():
                vertices += f"{index} {vertice}\n"

            for vertice, index in self.nameDict.items():
                for j, weight in enumerate(self.aMatrix[index]):
                    if not self.weighted and weight is not None:
                        edges += f"{index} {j}\n"
                    elif self.weighted and weight is not None:
                        edges += f"{index} {j} {weight}\n"
        
        finalString += configuration
        finalString += vertices
        # finalString += "\n\n"
        finalString += edges

        return finalString

############################# TDE 2 #################################

    def component_extraction(self):
        pass

    def degree_centrality(self, vertice:str)-> float:
        """Returns the degree centrality of a given vertice."""
        if self.representation == "LIST":
            vertices = self.aList
        elif self.representation == "MATRIX":
            vertices = self.nameDict

        return self.degree(vertice) / (len(vertices) - 1)

    def betweenness_centrality(self, vertice:str):
        """Counts the number of times a vertex appears on 
        the shortest path between any two other vertices."""

        if self.representation == "LIST":
            vertices = self.aList
        elif self.representation == "MATRIX":
            vertices = self.nameDict

        nodes_size:int = len(vertices)
        counter:int = 0 

        for v in vertices:
            if v != vertice:
                all_paths, _ = self.DJ_kstra(v)
                for x in vertices:
                    if x == vertice and x == v:
                        continue
                    if vertice in all_paths[x]:
                        counter += 1
                        

        return counter / ((nodes_size - 1) * (nodes_size - 2))


    def closeness_centrality(self, vertice:str):
        """Returns the closeness centrality of a given vertice."""
        if self.representation == "LIST":
            vertices = self.aList
        elif self.representation == "MATRIX":
            vertices = self.nameDict
        
        nodes_size:int = len(vertices)
        sum_distances:float = 0.0

        for v in vertices:
            if v != vertice:
                path, total_cost, total_time = self.dijkstra(v, vertice)
                sum_distances += total_cost

        return (nodes_size - 1) / sum_distances

    def eccentricity(self, vertice:str):
        if self.find_vertice(vertice) and self.is_connected():
            if self.representation == "LIST":
                vertices = self.aList
            elif self.representation == "MATRIX":
                vertices = self.nameDict
            ecc = 0
            for i in vertices:
                if i != vertice:
                    dijkstra, time3, cost = self.dijkstra(vertice, i, True)
                    print(f"dijkstra: {dijkstra}")
                    shortest = 0
                    if len(dijkstra) > shortest:
                        shortest = len(dijkstra)
                    if shortest > ecc:
                        ecc = shortest
            return ecc - 1
        return None


    def diameter(self):
        if self.is_connected():
            if self.representation == "LIST":
                vertices = self.aList
            elif self.representation == "MATRIX":
                vertices = self.nameDict
            diameter = 0
            for vertice in vertices:
                ecc = self.eccentricity(vertice)
                if ecc > diameter:
                    diameter = ecc
            return diameter

    def radius(self):
        if self.is_connected():
            if self.representation == "LIST":
                vertices = self.aList
            elif self.representation == "MATRIX":
                vertices = self.nameDict
            diameter = 1e10
            for vertice in vertices:
                ecc = self.eccentricity(vertice)
                if ecc < diameter:
                    diameter = ecc
            return diameter

    def edge_betweenness(self, parent:str, child:str):
        pass

    def all_paths(self):
        """Returns all shortest paths between all possible vertices."""
        if self.representation == "LIST":
            vertices = self.aList
        elif self.representation == "MATRIX":
            vertices = self.nameDict
        geo = []
        done = []
        for vertice in vertices:
            for vertice2 in vertices:
                if vertice != vertice2 and vertice2 not in done:
                    dijkstra, time3, cost = self.dijkstra(vertice, vertice2, True)
                    geo.append(dijkstra)
            done.append(vertice)
        return geo
    
    def geodesic_distance(self):
        """Returns total number of shortest paths between all possible vertices."""
        return len(self.all_paths())

    def girvan_newman(self):
        pass
                

############################# TESTS ###############################



gL = Graph(False, False, "LIST")
gM = Graph(False, False, "MATRIX")

# # print(gL.find_vertice("A"))
gL.add_vertice("A")
# print(gL.find_vertice("A"))
gL.add_vertice("B")
gL.add_vertice("C")
gL.add_vertice("D")
gL.add_vertice("E")


gM.add_vertice("A")
gM.add_vertice("B")
gM.add_vertice("C")
gM.add_vertice("D")
gM.add_vertice("E")


gL.add_edge("A", "C")
gL.add_edge("B", "A")
gL.add_edge("C", "A")
gL.add_edge("C", "D")
gL.add_edge("C", "E")
gL.add_edge("D", "E")
# print(gL.find_edge("A", "C"))
# print(gL.find_edge("B", "C"))

gM.add_edge("A", "C")
gM.add_edge("B", "A")
gM.add_edge("C", "A")
gM.add_edge("C", "D")
gM.add_edge("C", "E")
gM.add_edge("D", "E")
# print(gM.find_edge("A", "C"))
# print(gM.find_edge("B", "C"))

print(gL.is_connected())
print(gM.is_connected())

print(gL.eccentricity("A"))
print(gL.eccentricity("B"))
print(gL.eccentricity("C"))
print(gL.eccentricity("D"))
print(gL.eccentricity("E"))

print(gM.eccentricity("A"))
print(gM.eccentricity("B"))
print(gM.eccentricity("C"))
print(gM.eccentricity("D"))
print(gM.eccentricity("E"))

print(f"Diameter: {gL.diameter()}")
print(f"Diameter: {gM.diameter()}")

print(f"Radius: {gL.radius()}")
print(f"Radius: {gM.radius()}")

# # gL.remove_vertice("D")
# # gM.remove_vertice("D")

# # gL.remove_edge("C", "A")

# print(f"GL Adjacencies: {gL.get_adjacencies('D')}")
# print(f"GM Adjacencies: {gM.get_adjacencies('A')}")
# print(f"GM Adjacencies: {gM.get_adjacencies('B')}")
# print(f"GM Adjacencies: {gM.get_adjacencies('C')}")
# print(f"GM Adjacencies: {gM.get_adjacencies('D')}")

print(gL.all_paths())
print(gL.geodesic_distance())
print(gM.all_paths())
print(gM.geodesic_distance())

print(gM.degree_centrality("A"))
print(gM.degree_centrality("B"))
print(gM.degree_centrality("C"))
print(gM.degree_centrality("D"))
print(gM.degree_centrality("E"))


# # print(gL.get_weight("B", "C"))
# # print(gM.get_weight("B", "C"))

# print(gL.width_search("A", "D"))
# print(gL.depth_search("A", "D"))
# path, cost, t = gL.dijkstra("A", "D")
# print(f"Caminho entre A e D{path} com peso {cost} e tempo de {t} segundos")

# print(gM.width_search("A", "D"))
# print(gM.depth_search("A", "D"))
# path, cost, t = gM.dijkstra("A", "D")
# print(f"Caminho entre A e D{path} com peso {cost} e tempo de {t} segundos")

# print(gL)
print(gM)

# print(gL.aList)
print(gM.aMatrix)
print(gM.nameDict)


################# Weight Testing #################

# gMW = Graph(False, True, "MATRIX")
# gLW = Graph(False, True, "LIST")

# gLW.add_vertice("A")
# gLW.add_vertice("B")
# gLW.add_vertice("C")
# gLW.add_vertice("D")

# gLW.add_edge("A", "C", 4)
# gLW.add_edge("B", "A", 5)
# gLW.add_edge("C", "A", 3)
# gLW.add_edge("C", "D", 2)

# print(gLW.get_weight("A", "C"))

# gLW.set_weight("C", "A", 9)

# print(gLW.get_weight("A", "C"))
# print(gLW.get_weight("C", "A"))

# path, cost, t = gLW.dijkstra("A", "D")
# print(f"Caminho entre A e D{path} com peso {cost} e tempo de {t} segundos")

######################### Other Testing ########################

# print(gL.aList.keys())
# print(gM.nameDict.keys())

# a = gM.nameDict.keys()
# b = gL.aList.keys()

# print(b, a)

# for i in b:
#     print(i)