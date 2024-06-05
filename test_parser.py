from lib.Parser import Parser
from lib.Interpreter import Interpreter
from lib.Graph import Graph

p = Parser('data/tabela_artigos_limpa.csv')

interpreter: Interpreter = Interpreter()
extraction:dict = p.parse(configs={"directed": False, "weighted": True, "representation": "MATRIZ"})

interpreter.build(extraction)