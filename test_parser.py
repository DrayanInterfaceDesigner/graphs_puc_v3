from lib.Parser import Parser
from lib.Interpreter import Interpreter
from lib.Graph import Graph

p = Parser('data/tabela_artigos_limpa.csv')

interpreter: Interpreter = Interpreter()
extraction:dict = p.parse(configs={"directed": False, "weighted": True, "representation": "LIST"})

graph = interpreter.build(extraction)

# print(graph)

# 1) 
def most_productive():
    pairs = []
    for vertice in (graph.aList if graph.representation == "LIST" else graph.nameDict):
        adjacencies = graph.get_adjacencies(vertice)
        for adjacency in adjacencies:
            weight = graph.get_weight(vertice, adjacency)
            if not any((v == vertice and w == adjacency) or (v == adjacency and w == vertice) for v, w, p in pairs):
                pairs.append((vertice, adjacency, weight))
    return sorted(pairs, key=lambda x: x[2], reverse=True)[:10]

# print(most_productive())

# 2)
# print(len(graph.component_extraction()))

# 3)
# graph.degree_distribution_histogram()

# 4)
# print(sorted(graph.graph_degree_centrality().items(), key=lambda x: x[1], reverse=True)[:10])

# 5) demora pa um caray
# print(sorted(graph.graph_betweenness_centrality().items(), key=lambda x: x[1], reverse=True)[:10])

# 6) demora pa um caray 2: o retorno
# print(sorted(graph.graph_closeness_centrality().items(), key=lambda x: x[1], reverse=True)[:10])

# 7) demora pa um caray 3 e olha que eu nem botei os outros 4 subgrafos pra rodar. saporra nem chegou no pogger
# como o grafo nao eh conexo a função não pode rodar. Sendo assim, precisamos repartir o grafo em subgrafos e executar um por um (deus tende piedade de nós)
# sub = graph.girvan_newman(5) # 5 componentes que nem a gente viu na questão 2
# print("pogger!")
# print(sorted(sub[0].graph_closeness_centrality().items(), key=lambda x: x[1], reverse=True)[:10])

# 8) ver questão 7, inclusive faz até mais sentido fazer elas juntas porque a 8 depende da 7, mas é aquela coisa de que não é conexo então tem q fazer um por um.

# 9)
print(sorted(graph.graph_edge_betweenness().items(), key=lambda x: x[1], reverse=True)[:10])

# 10)
# sub = graph.girvan_newman(5) # 5 componentes que nem a gente viu na questão 2
# print("pogger!")
# botar função que compara o número de vértices de cada subgrafo aqui
# sub[0].avg_geodesic_distance()

# 11)
# sub = graph.girvan_newman(5) # 5 componentes que nem a gente viu na questão 2
# print("pogger!")
# botar função que compara o número de vértices de cada subgrafo aqui
# sub[0].girvan_newman(4)

# Temporizar essa caralha toda

