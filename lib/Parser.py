from datetime import datetime

class Parser:
    def __init__(self, file:str) -> None:
        self.file:str = file
        self.lines:list = []
        self.configs:list = []
        self.vertices:list = []
        self.connections:list = []
    
    # read the lines
    def read(self, path:str) -> None:
        with open(path) as file:
            # store the lines in the class
            self.lines = file.readlines()
    
    def save(self, graph) -> None:
        date:str = datetime.now().strftime("%Y%m%d%H%M%S")
        output:str = f"directed_{graph.directed}_weighted_{graph.weighted}_representation_{graph.representation}_{date}.net"
        with open(output, 'w') as file:
            file.write(graph.to_pajek())
        
    def reset(self) -> None:
        self.lines = []
        self.configs = []
        self.vertices = []
        self.connections = []
    
    # parse the configurations
    def parse_configs(self) -> None:

        # store the index of the last configuration
        max_index: int = 0
        # iterate over all lines
        for i in range(len(self.lines)):
            if self.lines[i].startswith("%"):
                # get the configuration fragment
                fragment: str = self.lines[i].replace("%", "").strip().split("=")

                # normalize the fragment
                property: str = fragment[0].lower()
                value: str = fragment[1].capitalize()

                # store the configuration
                self.configs.append({property: value})

                max_index = i

            # break out of the loop if it reaches the end of the configurations
            if self.lines[i].startswith("*"):
                break
        
        # clean off the used lines
        self.lines = self.lines[max_index+1:]
    
    def parse_vertices(self, from_index:int) -> None:
        for i in range(from_index, len(self.lines)):

            # break out of the loop if it reaches the end of the vertices
            if self.lines[i].startswith("*"):
                break
            else:
                # separate the line in a sentence
                sentence:str = self.lines[i].strip().split(" ")
                
                vertice_index:int = int(sentence[0])
                vertice_name:str = sentence[1]

                # store the vertice
                self.vertices.append({vertice_index: vertice_name})

    def parse_edges(self, from_index:int) -> None:
        for i in range(from_index, len(self.lines)):

            # break out of the loop if it reaches the end of the edges
            if self.lines[i].startswith("*"):
                break
            else:
                # separate the line in a sentence
                sentence:str = self.lines[i].strip().split(" ")
                
                parent_vertice:int = int(sentence[0])
                child_vertice:int = int(sentence[1])
                connection_weight:int = sentence[2] if len(sentence) > 2 else '1'

                # store the vertice
                self.connections.append({'parent': parent_vertice, 'child': child_vertice, 'weight': connection_weight})
    
    # parse the vertices and edges
    def parse_lines(self) -> None:
        for i in range(len(self.lines)):
            if self.lines[i].startswith("*"):

                # line normalization
                line:str = self.lines[i].replace("*", "").strip().upper()
                
                if line.startswith("VERTICES"):
                    self.parse_vertices(i+1)
                elif line == "EDGES" or line == "ARCS":
                    self.parse_edges(i+1)
    
    def parse(self, path:str='') -> dict:

        if path == '':
            path = self.file
        # reset the class just in case
        self.reset()

        # process stuff
        self.read(path)
        self.parse_configs()
        self.parse_lines()

        return {
            'configs': self.configs,
            'vertices': self.vertices,
            'connections': self.connections
        }
    
    