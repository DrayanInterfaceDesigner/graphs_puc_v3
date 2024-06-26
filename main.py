from lib.Parser import Parser
from lib.Interpreter import Interpreter
from lib.Graph import Graph

parser: Parser = Parser("data/graph.net")
interpreter: Interpreter = Interpreter()
extraction:dict = parser.parse()

def test_reading_pajek_file():
    print(f'\n =========== Test for reading pajek file =========== \n')

    parser: Parser = Parser("data/graph.net")
    interpreter: Interpreter = Interpreter()
    extraction:dict = parser.parse()

    graph = interpreter.build(extraction)
    print(graph)

def test_add_vertice():
    print(f'\n =========== Test for adding a new vertice =========== \n')

    graph = Graph(False, False, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    print(graph)

def test_add_existing_vertice():
    print(f'\n =========== Test for adding existing vertice =========== \n')

    graph = Graph(False, False, 'LIST')
    graph.add_vertice('A')
    graph.add_vertice('A')
    print(graph)

def test_add_edge_n_weighted():
    print(f'\n =========== Test for adding edge non weighted =========== \n')

    graph = Graph(False, False, 'MATRIX')
    graph_weighted = Graph(False, True, 'MATRIX')

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

    graph = Graph(False, True, 'LIST')
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

    graph = Graph(False, False, 'MATRIX')
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

    graph = Graph(False, False, 'LIST')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    # graph.add_edge('B', 'C')

    print(
        f'A out degree: {graph.out_degree("A")},',
        f'B out degree: {graph.out_degree("B")},',
        f'C out degree: {graph.out_degree("C")}', '\n'
    )

    print(
        f'A in degree: {graph.in_degree("A")},',
        f'B in degree: {graph.in_degree("B")},',
        f'C in degree: {graph.in_degree("C")}', '\n'
    )

    print(
        f'A degree: {graph.degree("A")},',
        f'B degree: {graph.degree("B")},',
        f'C degree: {graph.degree("C")}', '\n'
    )

def test_weight_update():
    print(f'\n =========== Test for weight update =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B', 2)
    graph.add_edge('B', 'C', 4)
    graph.add_edge('B', 'C', 6)

    print(graph)

    graph.set_weight('B', 'C', 6)

    print(graph)

    graph.set_weight('A', 'C', 3)

    print(graph)

def test_persistence():
    print(f'\n =========== Test for persistence =========== \n')

    graph = Graph(False, True, 'MATRIX')
    graph.add_vertice('A')
    graph.add_vertice('B')
    graph.add_vertice('C')
    graph.add_edge('A', 'B', 2)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('B', 'C', 6)

    parser.save(graph)

    print(graph)

    print("Check data folder!")

def test_transitive_closure():
    print(f'\n =========== Test for transitive closure =========== \n')

    graph = Graph(False, False, 'LIST')
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

    graph = Graph(True, True, 'LIST')

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
    print(graph)

    prim_graph, cost = graph.prim()
    print(f'MST: {prim_graph}\n cost = {cost}')

def test_degree_distribution_histogram():
    print(f'\n =========== Test for degree distribution histogram =========== \n')

    graph = Graph(True, False, 'MATRIX')

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

############################ TDE 2 ################################

def test_new_features():
    print(f'\n =========== Testing most new features in TDE2 =========== \n')
    gL = Graph(False, False, "LIST")
    gM = Graph(False, False, "MATRIX")

    gL.add_vertice("A")
    gL.add_vertice("B")
    gL.add_vertice("C")
    gL.add_vertice("D")
    gL.add_vertice("E")
    gM.add_vertice("A")
    gM.add_vertice("B")
    gM.add_vertice("C")
    gM.add_vertice("D")
    gM.add_vertice("E")
    gL.add_edge("A", "B")
    gL.add_edge("A", "C")
    gL.add_edge("C", "B")
    gL.add_edge("C", "D")
    gL.add_edge("B", "D")
    gL.add_edge("D", "E")
    gM.add_edge("A", "B")
    gM.add_edge("A", "C")
    gM.add_edge("C", "B")
    gM.add_edge("C", "D")
    gM.add_edge("B", "D")
    gM.add_edge("D", "E")

    print(gL)
    print(gM)

    print("eccentricity:")

    print(gL.graph_eccentricity())
    print(gM.graph_eccentricity())

    print(f"Diameter: {gL.diameter()}")
    print(f"Diameter: {gM.diameter()}")

    print(f"Radius: {gL.radius()}")
    print(f"Radius: {gM.radius()}")

    print("degree centrality:")

    print(gL.graph_degree_centrality())
    print(gM.graph_degree_centrality())

    print("closeness centrality:")

    print(gL.graph_closeness_centrality())
    print(gM.graph_closeness_centrality())

    print("betweenness centrality:")

    print(gL.graph_betweenness_centrality())
    print(gM.graph_betweenness_centrality())

    print("edge betweenness:")

    print(gL.graph_edge_betweenness())
    print(gM.graph_edge_betweenness())

    print("average geodesic distance:")
    
    print(gL.avg_geodesic_distance())
    print(gM.avg_geodesic_distance())

    print(gL)
    print(gM)

def test_girvan():
    print(f'\n =========== Testing girvan-newman =========== \n')
    girvan = Graph(False, False, "LIST")

    girvan.add_vertice("A")
    girvan.add_vertice("B")
    girvan.add_vertice("C")
    girvan.add_vertice("D")
    girvan.add_vertice("E")
    girvan.add_vertice("F")
    girvan.add_vertice("G")
    girvan.add_vertice("H")
    girvan.add_vertice("I")

    girvan.add_edge("A", "B")
    girvan.add_edge("B", "C")
    girvan.add_edge("C", "A")
    girvan.add_edge("D", "E")
    girvan.add_edge("E", "F")
    girvan.add_edge("F", "D")
    girvan.add_edge("C", "D")
    girvan.add_edge("G", "H")
    girvan.add_edge("H", "I")
    girvan.add_edge("I", "G")
    girvan.add_edge("F", "G")

    print(girvan)

    print("Running Girvan-Newman:\n")

    sub = girvan.girvan_newman(3)

    print(f"{sub[0]}\n {sub[1]}\n {sub[2]}")

def test_component_extraction():
    print(f'\n =========== Testing component extraction =========== \n')
    graph = Graph(False, False, "LIST")

    graph.add_vertice("A")
    graph.add_vertice("B")
    graph.add_vertice("C")
    graph.add_vertice("D")
    graph.add_vertice("E")
    graph.add_vertice("F")
    graph.add_vertice("G")
    graph.add_vertice("H")
    graph.add_vertice("I")

    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")
    graph.add_edge("D", "E")
    graph.add_edge("E", "F")
    graph.add_edge("F", "D")
    graph.add_edge("G", "H")

    print(graph)

    print(graph.component_extraction())

test_reading_pajek_file()
test_add_vertice()
test_add_edge_n_weighted()
test_add_existing_vertice()
test_remove_vertice()
test_remove_edge()
test_edge_exists()
test_degree_operations()
test_weight_update()
test_persistence()
test_transitive_closure()
test_search_algorithms()
test_eulerian()
test_prim()
test_degree_distribution_histogram()
############################# TDE 2 ################################
test_new_features()
test_girvan()
test_component_extraction()