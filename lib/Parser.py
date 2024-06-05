from datetime import datetime
import pandas as pd
import ast
class Parser:
    def __init__(self, file:str) -> None:
        self.file:str = file
        self.lines:list = []
        self.configs:list = []
        self.vertices:list = []
        self.connections:list = []
        self.is_csv:bool = True if file.endswith('.csv') else False

    # read the lines
    def read(self, path:str) -> None:
        with open(path) as file:
            # store the lines in the class
            self.lines = file.readlines()
    
    def read_csv(self, path:str) -> None:

        df:pd.DataFrame = pd.read_csv(path)
        df['NOMES_AJUSTADOS'] = df['NOMES_AJUSTADOS'].apply(ast.literal_eval)
        return df
    
    def data_to_graphdata(self, df:pd.DataFrame) -> (list | dict):
        vertices:list = list(set(df['NOMES_AJUSTADOS'].sum()))
        connections:dict = {}

        for v in vertices:
            connections[v] = {}

        for v in vertices:
            # exemplo de conexao
            # { 'author_name': { 'author_name': 2, 'author_name': 3 } } the number is the weight
            conn:dict = {}
            # busca os artigos que contém o vertice
            articles = df[df['NOMES_AJUSTADOS'].apply(lambda x: v in x)]
            # itera sobre os artigos
            for article in articles.iterrows():
                # itera sobre os autores do artigo
                for author in article[1]['NOMES_AJUSTADOS']:
                    # se o autor for diferente do vertice
                    if author != v:
                        if author not in conn:
                            conn[author] = 1
                        else:
                            conn[author] += 1
            connections[v] = conn
        return vertices, connections
    
    def save(self, graph) -> None:
        date:str = datetime.now().strftime("%Y%m%d%H%M%S")
        output:str = f"data/{graph.directed}_{graph.weighted}_{graph.representation}_{date}.net"
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

    def parse_vertices_csv(self, vertices:list) -> None:
        for i in range(len(vertices)):
            self.vertices.append({i: vertices[i]})
    
    def parse_edges_csv(self, connections:dict) -> None:
        for vertice, conn in connections.items():
            for v, w in conn.items():
                # get parent index in the vertices list
                parent_index:int = list(filter(lambda x: list(x.values())[0] == vertice, self.vertices))[0]
                # get child index in the vertices list
                child_index:int = list(filter(lambda x: list(x.values())[0] == v, self.vertices))[0]

                parent_index = list(parent_index.keys())[0]
                child_index = list(child_index.keys())[0]
                
                self.connections.append({'parent': parent_index, 'child': child_index, 'weight': w})
    
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
    
    def parse(self, path:str='', configs:dict=None) -> dict:

        if path == '':
            path = self.file
        # reset the class just in case
        self.reset()
        
        if not self.is_csv:
            # process stuff
            self.read(path)
            self.parse_configs()
            self.parse_lines()
        else:
            if configs is None:
                raise Exception(f"""Configs must be provided for csv files.
                                Example: {{"directed": False, "weighted": True, "representation": "MATRIZ"}}
                                """)
            
            # process stuff
            df:pd.DataFrame = self.read_csv(path)
            v, c = self.data_to_graphdata(df)
            self.parse_vertices_csv(v)
            self.parse_edges_csv(c)
            
            for key, value in configs.items():
                self.configs.append({key: str(value)})

            # transform weights to string
            for i in range(len(self.connections)):
                self.connections[i]['weight'] = str(self.connections[i]['weight'])

            # { 'directed': True, 'weighted': True, 'representation': 'MATRIZ' }
        return {
            'configs': self.configs,
            'vertices': self.vertices,
            'connections': self.connections,
            'was_csv': self.is_csv
        }
    


