from lib.Parser import Parser
from lib.Interpreter import Interpreter
from lib.Graph import Graph
import time
import copy
from datetime import datetime


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Execution time of {func.__name__}: {end_time - start_time} seconds")
        return result
    return wrapper

p = Parser('data/tabela_artigos_limpa.csv')

interpreter: Interpreter = Interpreter()
extraction:dict = p.parse(configs={"directed": False, "weighted": True, "representation": "LIST"})

graph = interpreter.build(extraction)
# print(graph)

# 1) 
@measure_time
def most_productive(graph):
    print("== Question 1 ==")
    pairs = []
    for vertice in (graph.aList if graph.representation == "LIST" else graph.nameDict):
        adjacencies = graph.get_adjacencies(vertice)
        for adjacency in adjacencies:
            weight = graph.get_weight(vertice, adjacency)
            if not any((v == vertice and w == adjacency) or (v == adjacency and w == vertice) for v, w, p in pairs):
                pairs.append((vertice, adjacency, weight))
    results = sorted(pairs, key=lambda x: x[2], reverse=True)[:20]
    return results

# print(most_productive())

# 2)
@measure_time
def components():
    print("== Question 2 ==")
    return len(graph.component_extraction())

# print(components())

# 3)
@measure_time
def histogram():
    print("== Question 3 ==")
    graph.degree_distribution_histogram()

# histogram()

# 4)
@measure_time
def deg_centrality():
    print("== Question 4 ==")
    return sorted(graph.graph_degree_centrality().items(), key=lambda x: x[1], reverse=True)[:10]

# print(deg_centrality())

# 5) demora pa um caray
@measure_time
def bet_centrality():
    print("== Question 5 ==")
    return sorted(graph.graph_betweenness_centrality().items(), key=lambda x: x[1], reverse=True)[:10]

# print(bet_centrality())

# # 6) demora pa um caray 2: o retorno
@measure_time
def clo_centrality():
    print("== Question 6 ==")
    return sorted(graph.graph_closeness_centrality().items(), key=lambda x: x[1], reverse=True)[:10]

# print(clo_centrality())

# 7, 8) demora pa um caray 3
# como o grafo nao eh conexo a função não pode rodar. Sendo assim, precisamos repartir o grafo em subgrafos e executar um por um (deus tende piedade de nós)
# Faremos a 8 junto porque girvan_newman demora meses pra rodar.
@measure_time
def exc_centrality():
    print("== Question 7, 8 ==")
    arr = []
    rad = []
    diam = []
    sub = graph.girvan_newman(5) # 5 componentes que nem a gente viu na questão 2
    for g in sub:
        arr.append(sub[g].graph_excentricity().items())
        rad.append(radius(g))
        diam.append(diameter(g))
    return (sorted(arr, key=lambda x: x[1], reverse=True)[:10]), rad, diam

@measure_time
def radius(subgraph:Graph):
    return subgraph.radius()

@measure_time
def diameter(subgraph:Graph):
    return subgraph.diameter()

# exc, rad, diam = exc_centrality()
# print(f"{exc}\n{rad}\n{diam}")

# 9)
@measure_time
def edge_bet():
    print("== Question 9 ==")
    return sorted(graph.graph_edge_betweenness().items(), key=lambda x: x[1], reverse=True)[:10]

# print(edge_bet())

# 10)
@measure_time
def avg_geo():
    print("== Question 10 ==")
    sub = graph.create_subgraphs() # 5 componentes que nem a gente viu na questão 2
    length = []
    for g in sub:
        vertices = g.aList if g.representation == "LIST" else g.nameDict
        length.append(len(vertices))
    return sub[length.index(max(length))].avg_geodesic_distance()

# print(avg_geo())

# 11)
@measure_time
def sub_sub():
    print("== Question 11 ==")
    sub = graph.create_subgraphs() # 5 componentes que nem a gente viu na questão 2
    length = []
    result = []
    for g in sub:
        vertices = g.aList if g.representation == "LIST" else g.nameDict
        length.append(len(vertices))
    sub2 = sub[length.index(max(length))].girvan_newman(4)
    for g in sub2:
        result.append(sorted(g.graph_degree_centrality().items(), key=lambda x: x[1], reverse=True)[:5])
    return result

# print(sub_sub())