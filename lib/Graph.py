import time
import matplotlib.pyplot as plt
from copy import deepcopy

''' TEMPLATE:

        if self.representation == "LIST":
            pass
        elif self.representation == "MATRIX":
            pass

'''

class Graph:
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
        if self.representation == "LIST":
            if name in self.aList:
                return True   
        elif self.representation == "MATRIX":
            if name in self.nameDict:
                return True
        return False

    def find_edge(self, parent:str, child:str) -> bool:
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
        if self.find_vertice(vertice):
            adjacencies = {}
            if self.representation == "LIST":
                for i in self.aList[vertice]:
                    adjacencies[i] = self.aList[vertice][i]
                return adjacencies
            elif self.representation == "MATRIX":
                for i in range(len(self.aMatrix[self.nameDict[vertice]])):
                    if self.aMatrix[self.nameDict[vertice]][i]:
                        for key, value in self.nameDict.items():
                            if value == i:
                                adjacencies[key] = self.nameDict[key]
                return adjacencies


    def get_weight(self, parent:str, child:str) -> (int|float|None):
        if self.find_edge(parent, child):
            if not self.weighted:
                return 1
            elif self.representation == "LIST":
                return self.aList[parent][child]
            elif self.representation == "MATRIX":
                print(self.nameDict[parent])
                return self.aMatrix[self.nameDict[parent]][self.nameDict[child]]

    def set_weight(self, parent:str, child:str, weight:int|float) -> None:
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
        if self.find_vertice(name):
            if self.directed:
                return self.in_degree(name) + self.out_degree(name)
            else:
                return self.out_degree(name)
            
    
    def depth_search(self, start:str, end:str) -> int:
        pass

    def width_search(self, start:str, end:str) -> int:
        pass

    def extract_min(self, q, costs):
        pass

    def djikstra(self, start:str, end:str) -> int:
        pass


    def is_connected(self):
        pass

    def prim(self):
        pass

    def eulerian(self):
        pass

    def warshall(self):
        pass

    def degree_distribution_histogram(self):
        pass
    

    def __str__(self): # REWRITE THIS!!!!!!!!!!!

        idx_vertex = 0
        string_1 = ""
        string_2 = ""
        string_representation = "Nós: "
        #verificar se é matriz ou lista antes de printar
        if self.representation == "LIST":

            for i in self.aList.keys():

                string_1 += f"{i}({idx_vertex}), "
                string_2 += f"{i}({idx_vertex}): "

                for j in self.aList[i].keys():

                    string_2 += f"{j}, "

                idx_vertex+=1

                string_2 = string_2[0:-2]+"\n"

            string_representation += string_1[0:-2]
            string_representation += "\nArestas(listas de adjacências):\n"
            string_representation += string_2
            
            #return f"Grafo {self.representation} {self.aList}" ####
            
            return string_representation
        
        elif self.representation == "MATRIX":

            for i in self.nameDict.keys():

                string_1 += f"{i}({self.nameDict[i]}), "
                string_2 += f"{i}({self.nameDict[i]}): "

                for j in self.aMatrix[self.nameDict[i]]:
                    
                    if j == None:

                        j = 0

                    string_2 += f"{j} "
                
                idx_vertex+=1
                string_2 += "\n"
            
            string_representation += string_1[0:-2]
            string_representation += "\nArestas(matriz):\n"
            string_representation += string_2

            return string_representation
                
            #return f"{self.aMatrix}\n Vértices e index {self.nameDict}"

############################# TESTS ###############################



gL = Graph(False, False, "LIST")
gM = Graph(False, False, "MATRIX")

# print(gL.find_vertice("A"))
gL.add_vertice("A")
# print(gL.find_vertice("A"))
gL.add_vertice("B")
gL.add_vertice("C")
gL.add_vertice("D")


gM.add_vertice("A")
gM.add_vertice("B")
gM.add_vertice("C")
gM.add_vertice("D")


gL.add_edge("A", "C")
gL.add_edge("B", "A")
gL.add_edge("C", "A")
gL.add_edge("C", "D")
# print(gL.find_edge("A", "C"))
# print(gL.find_edge("B", "C"))

gM.add_edge("A", "C")
gM.add_edge("B", "A")
gL.add_edge("C", "A")
gM.add_edge("C", "D")
# print(gM.find_edge("A", "C"))
# print(gM.find_edge("B", "C"))

gL.remove_vertice("D")
gM.remove_vertice("D")

# gL.remove_edge("C", "A")

print(f"GL Adjacencies: {gL.get_adjacencies('A')}")
print(f"GM Adjacencies: {gM.get_adjacencies('A')}")

# print(gL.get_weight("B", "C"))
# print(gM.get_weight("B", "C"))

print(gL)
print(gM)

print(gL.aList)
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

