from lib.Parser import Parser
from lib.Interpreter import Interpreter
from lib.Graph import Graph

parser: Parser = Parser("data/matrix.net")
interpreter: Interpreter = Interpreter()
extraction:dict = parser.parse()

def test_reading_pajek_file():
    print(f'\n =========== Test for reading pajek file =========== \n')

    parser: Parser = Parser("data/graph.net")
    interpreter: Interpreter = Interpreter()
    extraction:dict = parser.parse()

    graph = interpreter.build(extraction)
    print(graph)

def test_add_existing_vertice():
    print(f'\n =========== Test for adding existing vertice =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('A')
    print(graph)

def test_add_edge_n_weighted():
    print(f'\n =========== Test for adding edge non weighted =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph_weighted = Graph(False, False, 'MATRIX')

    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_edge('A', 'B')

    graph_weighted.add_vertice('A')
    graph_weighted.add_vertice('B')
    graph_weighted.add_edge('A', 'B', 2)

    print(graph)
    print(graph_weighted)

def test_remove_vertice():
    print(f'\n =========== Test for removing vertice =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'C')

    print(graph)

    graph.remove_vertice('B')

    print(graph)

def test_remove_edge():
    print(f'\n =========== Test for removing edge =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'C')

    print(graph)

    graph.remove_edge('A', 'B')

    print(graph)


def test_edge_exists():
    print(f'\n =========== Test for edge exists =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'C')

    print(graph.find_edge('A', 'B'))

def test_degree_operations():
    print(f'\n =========== Test for degree operations =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'C')

    print(
        f'A out degree: {graph.out_degree("A")}',
        f'B out degree: {graph.out_degree("B")}',
        f'C out degree: {graph.out_degree("C")}', '\n'
    )

    print(
        f'A in degree: {graph.in_degree("A")}',
        f'B in degree: {graph.in_degree("B")}',
        f'C in degree: {graph.in_degree("C")}', '\n'
    )

    print(
        f'A degree: {graph.degree("A")}',
        f'B degree: {graph.degree("B")}',
        f'C degree: {graph.degree("C")}', '\n'
    )

def test_weight_update():
    print(f'\n =========== Test for weight update =========== \n')

    graph = Graph(False, False, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B', 2)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('B', 'C', 6)

    print(graph)


def test_print():
    print(f'\n =========== Test for print =========== \n')

    graph = Graph(True, False, 'MATRIX')
    graph_list = Graph(False, True, 'LIST')

    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B', 2)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('B', 'C', 6)

    graph_list.add_vertice('A')
    graph_list.add_vertice('B')
    graph_list.add_vertice('C')
    graph_list.add_edge('A', 'B', 2)
    graph_list.add_edge('A', 'C', 4)
    graph_list.add_edge('B', 'C', 6)

    print('MATRIX GRAPH', graph)
    print('\nLIST GRAPH', graph_list)

def test_persistency():
    print(f'\n =========== Test for persistency =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B', 2)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('B', 'C', 6)

    parser.save(graph)

    print("Check data folder!")

def test_transitive_closure():
    print(f'\n =========== Test for transitive closure =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'C')

    print(graph)
    warshall = graph.warshall()
    print('WARSHALL', warshall)

def test_search_algorithms():
    print(f'\n =========== Test for search algorithms =========== \n')

    graph = Graph(False, True, 'MATRIX')

    graph.add_vertice('A')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_vertice('D')
    graph.add_vertice('E')
    graph.add_edge('A', 'B', 2)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('B', 'C', 6)
    graph.add_edge('D', 'C', 1)
    graph.add_edge('D', 'E', 2)
    graph.add_edge('C', 'E', 3)

    print("Depth-first search from A -> E:\n")
    path, time = graph.depth_search('A', 'E')
    print(f"Shortest path between A and E: {path}. found in time: {time}\n\n")

    print("Width-first search from A -> E:\n")
    path, time = graph.width_search('A', 'E')
    print(f"Shortest path between A and E: {path}. found in time: {time}\n\n")

    print("Dijkstra's algorithm:\n")
    path, cost, time = graph.dijkstra('A', 'E')
    print(f"Shortest path between A and E: {path} with cost: {cost}. found in time: {time}")


def test_eulerian():
    print(f'\n =========== Test for eulerian =========== \n')

    graph = Graph(True, True, 'MATRIX')

    graph.add_vertice('A')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_vertice('D')
    # graph.add_vertice('E')
    graph.add_edge('A', 'B', 2)
    # graph.add_edge('A', 'C', 4)
    graph.add_edge('B', 'C', 6)
    graph.add_edge('C', 'D', 1)
    graph.add_edge('D', 'A', 2)
    # graph.add_edge('C', 'E', 3)

    print(graph)
    print("\nIs eulerian: ", graph.eulerian())

def test_prim():
    print(f'\n =========== Test for prim =========== \n')

    graph = Graph(False, True, 'LIST')

    graph.add_vertice('A')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_vertice('D')
    graph.add_vertice('E')
    graph.add_edge('A', 'B', 2)
    graph.add_edge('B', 'C', 4)
    graph.add_edge('C', 'D', 6)
    graph.add_edge('D', 'E', 7)
    graph.add_edge('E', 'A', 2)
    graph.add_edge('C', 'E', 3)

    prim_graph, cost = graph.prim()
    print(f'MST: {prim_graph}\n cost = {cost}')

def test_degree_distribution_histogram():
    print(f'\n =========== Test for degree distribution histogram =========== \n')

    graph = Graph(True, True, 'MATRIX')

    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_vertice('D')
    graph.add_vertice('E')

    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('A', 'D')
    graph.add_edge('B', 'C')
    graph.add_edge('B', 'E')

    graph.degree_distribution_histogram()



test_reading_pajek_file()
test_add_existing_vertice()
test_add_edge_n_weighted()
test_remove_vertice()
test_remove_edge()
test_edge_exists()
test_degree_operations()
test_weight_update()
test_print()
test_persistency()
test_transitive_closure()
test_search_algorithms()
test_eulerian()
test_prim()
test_degree_distribution_histogram()


# graph.add_vertice('A')
# graph.add_vertice('A')
# graph.add_vertice('B')
# graph.add_vertice('C')
# graph.add_vertice('D')
# graph.add_vertice('E')
# graph.add_edge('A', 'B', 2)
# graph.add_edge('A', 'C', 4)
# graph.add_edge('B', 'C', 6)
# graph.add_edge('D', 'C', 1)
# graph.add_edge('D', 'E', 2)
# graph.add_edge('C', 'E', 3)
# graph.remove_vertice('A')
# graph.remove_edge('A', 'B')

# graph.remove_vertice('D')

# print(graph.get_weight('A', 'B'))
# graph.set_weight('A', 'B', 50)
# graph.set_weight('C', 'A', 25)
# print(graph.get_weight('A', 'B'))

# print(graph.get_weight('A', 'B'))
# graph.set_weight('A', 'B', 50)
# graph.set_weight('C', 'A', 25)
# print(graph.get_weight('A', 'B'))

# print(
#     f'A out degree: {graph.out_degree("A")}',
#     f'B out degree: {graph.out_degree("B")}',
#     f'C out degree: {graph.out_degree("C")}',
# )

# print(
#     f'A in degree: {graph.in_degree("A")}',
#     f'B in degree: {graph.in_degree("B")}',
#     f'C in degree: {graph.in_degree("C")}',
# )

# print(
#     f'A degree: {graph.degree("A")}',
#     f'B degree: {graph.degree("B")}',
#     f'C degree: {graph.degree("C")}',
# )


# print(graph.get_adjacencies('A'))
# print(graph.get_adjacencies('B'))
# print(graph.get_adjacencies('C'))
# print(graph.get_adjacencies('A'))

# print("depth search A -> E")
# print(graph.depth_search('A', 'E'))

# print("width search A -> E")
# print(graph.width_search('A', 'E'))

# print(graph.vertices)

# path, cost, time = graph.dijkstra('A', 'E')
# print(f"Shortest path between A and E: {path} with cost: {cost}. found in time: {time}")

# print('Prim MST')
# g_mst, custo = graph.prim()
# print(f'MST = {g_mst}\n custo = {custo}')

# print(graph)

# parser.save(graph)

# graph.degree_distribution_histogram()

# print(graph.generate_matrix())

# graph.warshall()
