from lib.Parser import Parser
from lib.Interpreter import Interpreter

parser: Parser = Parser()
interpreter: Interpreter = Interpreter()
extraction:dict = parser.parse("tests/matrix.net")

print(interpreter.build(extraction))



print(extraction)
# print(interpreter.interpret_configurations(extraction['configs']))