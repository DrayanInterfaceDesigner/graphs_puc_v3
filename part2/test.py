from igraph import Graph

g = Graph()

g.add_vertices(
    ["A", "B", "C", "D", "E"]
)

g.add_edges(
    [
("A", "B"),
("A", "E"),
("B", "C"),
("B", "D"),
("D", "E"),
("C", "E"),
("C", "D")
    ]
)

# Calcular a centralidade de intermediação das arestas
centralidade_intermediação_arestas = g.edge_betweenness()

# Obter os índices das 10 arestas mais relevantes
indices_arestas_mais_relevantes_intermediação = sorted(range(len(centralidade_intermediação_arestas)), key=lambda i: centralidade_intermediação_arestas[i], reverse=True)[:10]

# Exibir as 10 arestas mais relevantes
for indice in indices_arestas_mais_relevantes_intermediação:
    fonte = g.es[indice].source
    destino = g.es[indice].target
    print(f"Aresta: {g.vs[fonte]['name']} - {g.vs[destino]['name']}, Centralidade de Intermediação: {centralidade_intermediação_arestas[indice]}")


import numpy as np


class Grap:
    def __init__(self) -> None:
        pass
    
    def edgeBetweenness(self, s, t):
        # Calculates the betweenness of a given edge s, t

        def qtdShortestPaths(verticeInicial, verticeFinal):
            # Retorna quantos caminhos mais curtos existem entre dois vértices
            allPaths = self.pathFinder(verticeInicial)
            qtdShortestPaths = {destination: len(paths) for destination, paths in allPaths.items() if destination != verticeInicial}
            return qtdShortestPaths.get(verticeFinal, 0)

        def shortestPathsEdge(verticeInicial, verticeFinal):
            # Retorna todos os caminhos mais curtos entre dois vértices
            allPaths = self.pathFinder(verticeInicial)
            return allPaths.get(verticeFinal, [])

        edge = (s, t)
        betweenness = 0.0

        vertices = np.array(self.vertices)
        for u in vertices:
            for v in vertices:
                if u != v:
                    totalPaths = qtdShortestPaths(u, v)
                    if totalPaths > 0:
                        pathsThroughE = 0
                        allPaths = shortestPathsEdge(u, v)
                        for path in allPaths:
                            edges_in_path = list(zip(path, path[1:]))
                            if edge in edges_in_path:
                                pathsThroughE += 1
                        betweenness += pathsThroughE / totalPaths

        return betweenness
    
    def allEdgesBet(self):
      # Returns the betweenness of all edges as a dictionary
      allEdgesBet = {}
      vertices = np.array(self.vertices)
      for s in vertices:
          for t in vertices:
              if s != t:  # não precisamos de um caminho de um vértice pra ele mesmo
                  edgeBet = self.edgeBetweenness(s, t)
                  if edgeBet > 0:
                      if not self.direcionado:  # adiciona o mesmo valor tanto para s, t quanto para t, s
                          allEdgesBet[(s, t)] = f"{edgeBet:.3f}"
                          allEdgesBet[(t, s)] = f"{edgeBet:.3f}"
                      else:
                          allEdgesBet[(s, t)] = f"{edgeBet:.3f}"

      return allEdgesBet
    
    def pegaVizinhos(self, vertice1):
        if self.repr == "matriz":
            vizinhos = []

            indiceV1 = self.vertices.index(vertice1)
            for vertice in self.vertices:
                indiceV2 = self.vertices.index(vertice)

                if self.matrizAdjacencias[indiceV1][indiceV2] != 0:
                    vizinhos.append(vertice)

            return vizinhos
        else: # lista
            if vertice1 in self.vertices:
                    vizinhos = [vizinho for (vizinho, _) in self.listaDict[vertice1]]
                    return vizinhos
            else:
                    return []