from lib.Parser import Parser
from lib.Interpreter import Interpreter
from lib.Graph import Graph

parser: Parser = Parser()
interpreter: Interpreter = Interpreter()
extraction:dict = parser.parse("tests/matrix.net")

# print(interpreter.build(extraction))

print(extraction)
# print(interpreter.interpret_configurations(extraction['configs']))


graph = Graph(True, True, 'MATRIZ')

graph.add_vertice('A')
graph.add_vertice('A')
graph.add_vertice('B')
graph.add_vertice('C')
graph.add_edge('A', 'B', 5)
graph.add_edge('B', 'A', 10)
graph.add_edge('B', 'C', 5)
# graph.remove_vertice('A')
# graph.remove_edge('A', 'B')

graph.remove_vertice('D')

print(
    f'A out degree: {graph.out_degree("A")}',
    f'B out degree: {graph.out_degree("B")}',
    f'C out degree: {graph.out_degree("C")}',
)

print(
    f'A in degree: {graph.in_degree("A")}',
    f'B in degree: {graph.in_degree("B")}',
    f'C in degree: {graph.in_degree("C")}',
)

print(
    f'A degree: {graph.degree("A")}',
    f'B degree: {graph.degree("B")}',
    f'C degree: {graph.degree("C")}',
)

print(graph.get_adjacent('A'))

print(graph)