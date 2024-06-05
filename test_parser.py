from lib.Parser import Parser
from lib.Interpreter import Interpreter
from lib.Graph import Graph
import time
import copy
from datetime import datetime

save_path = f"data/{datetime.now().strftime('%Y%m%d%H%M%S')}_results.txt"

def write_results_to_txt(results, filename):
    with open(filename, 'w') as f:
        for result in results:
            f.write(f"{result}\n")

def append_time_taken_to_txt(func_name, time_taken, filename):
    with open(filename, 'a') as f:
        f.write(f"{func_name} took {time_taken} seconds\n =============== \n")
    
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Execution time of {func.__name__}: {end_time - start_time} seconds")
        append_time_taken_to_txt(func.__name__, end_time - start_time, save_path)
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
    print(results)
    write_results_to_txt(results, save_path)
    print("========================================")
    return results

# print(most_productive())

# 2)
# print(len(graph.component_extraction()))

# 3)
# graph.degree_distribution_histogram()

# 4)
# print(sorted(graph.graph_degree_centrality().items(), key=lambda x: x[1], reverse=True)[:10])

# 5) demora pa um caray

@measure_time
def question5(graph):
    print("== Question 5 ==")
    result = sorted(graph.graph_betweenness_centrality().items(), key=lambda x: x[1], reverse=True)[:20]
    print(result)
    write_results_to_txt(result, save_path)
    print("========================================")
    return result
gc_5 = copy.deepcopy(graph)

# print(sorted(graph.graph_betweenness_centrality().items(), key=lambda x: x[1], reverse=True)[:10])

# 6) demora pa um caray 2: o retorno
@measure_time
def question6(graph):
    print("== Question 6 ==")
    result = sorted(graph.graph_closeness_centrality().items(), key=lambda x: x[1], reverse=True)[:20]
    print(result)
    write_results_to_txt(result, save_path)
    print("========================================")
    return result
gc_6 = copy.deepcopy(graph)

# print(sorted(graph.graph_closeness_centrality().items(), key=lambda x: x[1], reverse=True)[:10])

# 7) demora pa um caray 3 e olha que eu nem botei os outros 4 subgrafos pra rodar. saporra nem chegou no pogger
# como o grafo nao eh conexo a função não pode rodar. Sendo assim, precisamos repartir o grafo em subgrafos e executar um por um (deus tende piedade de nós)
# sub = graph.girvan_newman(5) # 5 componentes que nem a gente viu na questão 2
# print("pogger!")
# print(sorted(sub[0].graph_closeness_centrality().items(), key=lambda x: x[1], reverse=True)[:10])

@measure_time
def question7(graph):
    print("== Question 7 ==")
    sub = graph.girvan_newman(5)
    result = sorted(sub[0].graph_closeness_centrality().items(), key=lambda x: x[1], reverse=True)[:20]
    print(result)
    write_results_to_txt(result, save_path)
    print("========================================")
    return result
gc_7 = copy.deepcopy(graph)

# 8) ver questão 7, inclusive faz até mais sentido fazer elas juntas porque a 8 depende da 7, mas é aquela coisa de que não é conexo então tem q fazer um por um.

# 9)
# print(sorted(graph.graph_edge_betweenness().items(), key=lambda x: x[1], reverse=True)[:10])

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


most_productive(graph)
# question5(gc_5)
# question6(gc_6)
# question7(gc_7)

