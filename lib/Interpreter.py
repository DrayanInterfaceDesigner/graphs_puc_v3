from lib.Graph import Graph

class Interpreter:
    def __init__(self) -> None:
        pass

    def infer_type(self, value:str) -> type:
        if value.isdigit():
            return int(value)
        elif value.replace(".", "", 1).isdigit():
            return float(value)
        else:
            try:
                if value.lower() == "true":
                    return True
                elif value.lower() == "false":
                    return not True
                else:
                    return str(value)
            except:
                return str(value)

    def interpret_configurations(self, parsed_configurations:dict) -> None:
        config:dict = {}
        for configuration in parsed_configurations:
            for property, value in configuration.items():
                config[property] = self.infer_type(value)
        return config

    def interpret_vertices(self, graph:Graph, parsed_vertices:dict) -> None:
        for vertice in parsed_vertices:
            for index, name in vertice.items():
                graph.add_vertice(name)
    
    def interpret_edges(self, graph:Graph, parsed:dict) -> None:
        connections:list = parsed['connections']
        vertices:list = parsed['vertices']

        for connection in connections:
            
            graph.add_edge(
                list(vertices[connection['parent']].values())[0], 
                list(vertices[connection['child']].values())[0], 
                self.infer_type(connection['weight'])
            )

    def build(self, parsed:dict) -> Graph:
        config:dict = self.interpret_configurations(parsed['configs'])

        graph:Graph = Graph(
            config.get('directed'),
            config.get('weighted'),
            config.get('representation').upper()
        )

        self.interpret_vertices(graph, parsed['vertices'])
        self.interpret_edges(graph, parsed)
        
        return graph