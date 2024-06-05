import numpy as np
import pandas as pd
import ast
from igraph import Graph, VertexClustering
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Execution time of {func.__name__}: {end_time - start_time} seconds")
        return result
    return wrapper

df = pd.read_csv('data/tabela_artigos_limpa.csv')
df['NOMES_AJUSTADOS'] = df['NOMES_AJUSTADOS'].apply(ast.literal_eval)
print(df.head())

@measure_time
def data_to_graphdata(df:pd.DataFrame) -> (list | dict):
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
                    # se o vertice ainda não tiver conexão com o autor
                    if author not in conn:
                        conn[author] = 1
                    else:
                        conn[author] += 1
        connections[v] = conn
    return vertices, connections

vertices, connections = data_to_graphdata(df)
# for


print(connections)
exit()

g = Graph()
g.add_vertices(vertices)

@measure_time
def add_edges(graph:Graph, connections:dict) -> None:
    for v, conn in connections.items():
        for c, w in conn.items():
            graph.add_edge(v, c, weight=w)

add_edges(g, connections)




print(g.summary())
print("====================================")

# ========================================================================================================================

print("====================================")
print("1) Question:")

# 1) Quais pares de autores são os mais produtivos dentro da rede? Elenque os 10 pares de autores
# mais produtivos da rede

# Obter todas as arestas com seus pesos
arestas_pesos = [(e.source, e.target, e["weight"]) for e in g.es]

# Ordenar as arestas pelo peso (em ordem decrescente)
arestas_pesos.sort(key=lambda x: x[2], reverse=True)

# Selecionar os 10 pares mais produtivos
pares_mais_produtivos = arestas_pesos[:20]

# Exibir os pares mais produtivos
print("10 pares de autores mais produtivos:")
for par in pares_mais_produtivos:
    print(f"- Autores: {g.vs[par[0]]['name']} - {g.vs[par[1]]['name']}, Colaborações: {par[2]}")


# ========================================================================================================================

print("====================================")
print("2) Question:")

# 2) Quantas componentes o grafo possui?

# # Obter todas as arestas com seus pesos
# arestas_pesos = [(e.source, e.target, e["weight"]) for e in g.es]

# # Ordenar as arestas pelo peso (em ordem decrescente)
# arestas_pesos.sort(key=lambda x: x[2], reverse=True)

# # Selecionar os 10 pares mais produtivos
# pares_mais_produtivos = arestas_pesos[:20]

# # Exibir os pares mais produtivos
# for par in pares_mais_produtivos:
#     print(f"Autores: {g.vs[par[0]]['name']} - {g.vs[par[1]]['name']}, Colaborações: {par[2]}")

num_componentes = len(g.connected_components())
print(f"O grafo possui {num_componentes} componente(s).")

# O que isso representa?

# num_componentes = 1: O grafo é conexo. Todos os autores estão conectados por meio de colaborações, direta ou indiretamente.
# num_componentes > 1: O grafo é desconexo. Existem autores ou grupos de autores que não colaboraram com outros autores ou grupos. 
# Cada componente representa um grupo isolado de autores que colaboraram entre si.
# Exemplo:

# Se num_componentes = 3, significa que existem três grupos distintos de autores na rede. 
# Dentro de cada grupo, os autores colaboraram entre si, mas não houve colaboração entre autores de grupos diferentes.

# ========================================================================================================================

print("====================================")
print("4) Question:")

# 4) Quais são os 10 autores mais influentes perante a métrica de centralidade de grau? 

# Calcular a centralidade de grau para todos os vértices
centralidade_grau = g.degree()

# Criar um dicionário que mapeia o nome do autor à sua centralidade de grau
centralidade_por_autor = {g.vs[i]["name"]: centralidade_grau[i] for i in range(g.vcount())}

# Ordenar os autores pela centralidade de grau em ordem decrescente
autores_ordenados = sorted(centralidade_por_autor.items(), key=lambda item: item[1], reverse=True)

# Selecionar os 10 autores mais influentes
top_10_influentes = autores_ordenados[:20]

# Exibir os 10 autores mais influentes
print("10 autores mais influentes (centralidade de grau):")
for autor, centralidade in top_10_influentes:
    print(f"- Autor: {autor}, Centralidade de Grau: {centralidade}")

# O que essa métrica representa nesse contexto?

# No contexto de autores, a centralidade de grau mede o número de conexões (citações, colaborações, etc.) 
# que um autor tem com outros autores. Quanto maior o grau de centralidade, mais influente é o autor na rede.


# ========================================================================================================================

print("====================================")
print("5) Question:")

# 5) Quais são os 10 autores mais influentes perante a métrica de centralidade de intermediação?

# Calcular a centralidade de intermediação para todos os vértices
betweenness = g.betweenness(weights="weight")

# Criar um dicionário mapeando vértices (índices) à sua centralidade de intermediação
betweenness_dict = {v: betweenness[i] for i, v in enumerate(g.vs)}

# Ordenar os autores pela centralidade de intermediação (em ordem decrescente)
autores_ordenados = sorted(betweenness_dict.items(), key=lambda x: x[1], reverse=True)

# Selecionar os 10 autores mais influentes
top_10_influentes = autores_ordenados[:20]

# Exibir os 10 autores mais influentes pela centralidade de intermediação
print("\n10 autores mais influentes (centralidade de intermediação):")
for autor, centralidade in top_10_influentes:
    print(f"- Autor: {autor['name']}, Centralidade: {centralidade:.4f}") 

# O que essa métrica representa nesse contexto?

# A centralidade de intermediação (betweenness centrality) mede o quão frequentemente um vértice (autor, no nosso caso) 
# aparece nos caminhos mais curtos entre outros pares de vértices.
# Autores com alta intermediação são como "pontes" que conectam diferentes partes da rede.

# ========================================================================================================================

print("====================================")
print("6) Question:")

# 6) Quais são os 10 autores mais influentes perante a métrica de centralidade de proximidade?
# O que essa métrica representa nesse contexto?

# Calcular a centralidade de proximidade para todos os vértices
closeness = g.closeness(weights="weight")  # Usamos os pesos para levar em conta a força das colaborações

# Criar um dicionário mapeando vértices (índices) à sua centralidade de proximidade
closeness_dict = {v: closeness[i] for i, v in enumerate(g.vs)}

# Ordenar os autores pela centralidade de proximidade (em ordem decrescente)
autores_ordenados = sorted(closeness_dict.items(), key=lambda x: x[1], reverse=True)

# Selecionar os 10 autores mais influentes
top_10_influentes = autores_ordenados[:20]

# Exibir os 10 autores mais influentes pela centralidade de proximidade
print("\n10 autores mais influentes (centralidade de proximidade):")
for autor, centralidade in top_10_influentes:
    print(f"- Autor: {autor['name']}, Centralidade: {centralidade:.4f}")

# A centralidade de proximidade (closeness centrality) mede o quão próximo um vértice (autor)
# está de todos os outros vértices na rede.
# Autores com alta proximidade podem disseminar informações de forma mais rápida e eficiente.


# ========================================================================================================================

print("====================================")
print("7) Question:")

# 7) Quais são os 10 autores mais influentes perante a métrica de centralidade de excentricidade?

# Calcular a centralidade de excentricidade para todos os vértices
eccentricity = g.eccentricity()

# Criar um dicionário mapeando vértices (índices) à sua centralidade de excentricidade
eccentricity_dict = {v: eccentricity[i] for i, v in enumerate(g.vs)}

# Ordenar os autores pela centralidade de excentricidade (em ordem crescente, pois menor excentricidade significa mais central)
autores_ordenados = sorted(eccentricity_dict.items(), key=lambda x: x[1])

# Selecionar os 10 autores mais influentes (com menor excentricidade)
top_10_influentes = autores_ordenados[:20]

# Exibir os 10 autores mais influentes pela centralidade de excentricidade
print("\n10 autores mais influentes (centralidade de excentricidade):")
for autor, centralidade in top_10_influentes:
    print(f"- Autor: {autor['name']}, Centralidade: {centralidade}")



# O que essa métrica representa nesse contexto?

# A centralidade de excentricidade (eccentricity centrality) mede a distância máxima de um vértice (autor) 
# a qualquer outro vértice na rede. 
# Autores com baixa excentricidade estão mais próximos do "centro" da rede e podem ter acesso mais rápido a informações e recursos.

# ========================================================================================================================

print("====================================")
print("8) Question:")


# 8) Calcule o diâmetro e o raio do grafo. 

# Calculando o diâmetro
diametro = g.diameter()

# Calculando o raio
raio = g.radius()

print(f"Diâmetro do grafo: {diametro}")
print(f"Raio do grafo: {raio}")

# O que essas métricas representam nesse contexto?
# O diâmetro de um grafo é a maior distância entre qualquer par de vértices, enquanto o raio é a menor distância 
# máxima de um vértice a todos os outros. Vamos calcular essas métricas usando a biblioteca igraph.

# Como o peso das arestas representa a força das colaborações, vamos considerar os 
# pesos no cálculo do diâmetro e do raio. Isso nos dará uma noção mais precisa da "distância" entre os autores, 
# levando em conta a intensidade das colaborações.

# ========================================================================================================================

print("====================================")
print("9) Question:")


# 9) Quais são as 10 arestas mais relevantes no grafo perante a métrica de centralidade de
# intermediação? 

# Calcular a centralidade de intermediação das arestas
centralidade_intermediação_arestas = g.edge_betweenness()

# Obter os índices das 10 arestas mais relevantes
indices_arestas_mais_relevantes_intermediação = sorted(range(len(centralidade_intermediação_arestas)), key=lambda i: centralidade_intermediação_arestas[i], reverse=True)[:20]

# Exibir as 10 arestas mais relevantes
for indice in indices_arestas_mais_relevantes_intermediação:
    fonte = g.es[indice].source
    destino = g.es[indice].target
    print(f"Aresta: {g.vs[fonte]['name']} - {g.vs[destino]['name']}, Centralidade de Intermediação: {centralidade_intermediação_arestas[indice]}")

# Dentre essas arestas, há algum comportamento que se destaca?

# As arestas mais relevantes em termos de centralidade de intermediação são aquelas que conectam grupos de autores. Como por exemplo,
# ...

# ========================================================================================================================

print("====================================")
print("10) Question:")


# 10) Qual é a média das distâncias geodésicas da maior componente do grafo?

# Encontrar a maior componente conexa
maior_componente = g.connected_components().giant()

# Calcular as distâncias geodésicas dentro da maior componente
distancias = maior_componente.distances(weights="weight")

# Calcular a média das distâncias (ignorando distâncias infinitas)
distancias_finitas = [d for linha in distancias for d in linha if d != float('inf')]
media_distancia = sum(distancias_finitas) / len(distancias_finitas)

print("Média das distâncias geodésicas na maior componente:", media_distancia)

# O que essa métrica representa nesse contexto?

# A distância geodésica entre dois vértices (autores, no nosso caso) é o menor número de arestas (colaborações) 
# que você precisa percorrer para ir de um vértice
#  ao outro. No contexto de colaborações, isso nos diz quantas conexões intermediárias existem entre dois autores.

# ========================================================================================================================

print("====================================")
print("11) Question:")

# 11) Dentro do grafo, encontre a componente com a maior quantidade de vértices. Dentro desta componente, 
# execute o algoritmo de Girvan-Newman e encontre as quatro principais comunidades. 
# Para cada comunidade, identifique e discuta os autores mais significativos de acordo com as métricas que julgar mais adequado.

# Maior Componente:

# Encontrar a maior componente conexa
componentes = g.components()
maior_componente = componentes.giant()

# Criar um subgrafo com a maior componente
subgrafo_maior_componente = maior_componente.subgraph(maior_componente.vs)

# Aplicando o Algoritmo de Girvan-Newman:

# Aplicar o algoritmo de Girvan-Newman
comunidades_dendrograma = subgrafo_maior_componente.community_edge_betweenness()
comunidades_cluster = comunidades_dendrograma.as_clustering(n=4)  # Dividir em 4 comunidades

# Identificando e Analisando as Comunidades:

# Métricas para avaliar a significância dos autores
for i, comunidade in enumerate(comunidades_cluster):
    print(f"\nComunidade {i+1}:")

    # Autores na comunidade
    autores_comunidade = [subgrafo_maior_componente.vs[v]["name"] for v in comunidade]
    print(f"Autores: {autores_comunidade}")

    # Métricas de centralidade
    centralidade_grau = subgrafo_maior_componente.degree(comunidade)
    centralidade_betweenness = subgrafo_maior_componente.betweenness(comunidade)

    # Encontrar o autor mais central em cada métricafaça com
    autor_grau_max = autores_comunidade[centralidade_grau.index(max(centralidade_grau))]
    autor_betweenness_max = autores_comunidade[centralidade_betweenness.index(max(centralidade_betweenness))]

    print(f"Autor mais central (grau): {autor_grau_max}")
    print(f"Autor mais central (betweenness): {autor_betweenness_max}")


# Grau (Degree): Indica o número de conexões diretas de um autor. Autores com alto grau são "hubs" na rede, 
# colaborando com muitos outros.

# Betweenness: Mede a frequência com que um autor aparece nos caminhos mais curtos entre outros autores. 
# Alto betweenness indica um papel de "ponte" entre diferentes partes da comunidade.

# Closeness: (Opcional) Mostra o quão próximo um autor está, em média, de todos os outros na rede.