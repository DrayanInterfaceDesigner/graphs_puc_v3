
class Grafo:

    def __init__(self, representacao, direcionado, ponderado):
        self.representacao = representacao
        self.direcionado = direcionado
        self.ponderado = ponderado
        # constroi lista de vertices
        self.lista_vertices = []
        # cria estrutura de representacao
        if self.representacao == 'matriz':
            # construo a matriz
            pass
        else: # lista
            # construo a lista de adjacencias
            # chave = vertice
            # valor = lista de vizinhos e os pesos
            self.dict_vizinhos = {}
    def adiciona_vertice(self, vertice):
        if vertice not in self.lista_vertices:
            self.lista_vertices.append(vertice)
            # se estou usando representacao de lista e
            # o vertice é novo, criamos uma lista vazia
            # de vizinhos para ele
            if self.representacao != 'matriz':
                self.dict_vizinhos[vertice] = []

    def cria_aresta(self, vertice_a, vertice_b, peso=1):
        # verifico se os vertices existem
        if vertice_a in self.lista_vertices and \
                vertice_b in self.lista_vertices:
            if self.representacao == 'matriz':
                pass
                # implementar depois
            else: #lista
                self.dict_vizinhos[vertice_a].\
                    append((vertice_b, peso))
                if not self.direcionado:
                    # cria conexao no sentido oposto tb
                    self.dict_vizinhos[vertice_b].\
                        append((vertice_a, peso))

    def remove_vertice(self, vertice_a):
        pass

    def remove_aresta(self, vertice_a, vertice_b):
        pass

    def atualiza_peso(self, vertice_a, vertice_b, peso):
        pass

    def existe_aresta(self, vertice_a, vertice_b):
        # verifico se os dois vertices existem
        if vertice_a in self.lista_vertices and \
                vertice_b in self.lista_vertices:
            # pego a lista de todos os vizinhos de A
            for t in self.dict_vizinhos[vertice_a]:
                # se eu encontrar o B, é vizinho :)
                if t[0] == vertice_b:
                    return True
        return False

    def indegree(self, vertice):
        pass

    def outdegree(self, vertice):
        pass

    def degree(self, vertice):
        pass

    def warshall(self):
        pass

    def dijkstra(self, vertice_a, vertice_b):
        # criar lista de predecessores
        pi = {}
        # estrutura de custo acumulado
        custos_acumulados = {}
        for vertice in self.lista_vertices:
            custos_acumulados[vertice] = +1e10 # "infinito"
            pi[vertice] = None

        # nó de saída tem custo zero
        custos_acumulados[vertice_a] = 0.0

        # Criar lista de prioridade (Q)
        q = []
        for vertice in self.lista_vertices:
            q.append(vertice)

        # loop principal
        while len(q) > 0:
            # encontra o nó com menor custo até o momento
            no_atual = self.extract_min(q, custos_acumulados)
            # não encontrei um nó, então saio do laço
            if no_atual is None:
                break
            q.remove(no_atual)

            # laço de repetição para verificar vizinhos
            for vizinho in self.pega_vizinhos(no_atual):
                print(no_atual, vizinho, self.pega_peso(no_atual, vizinho))
                # estima o custo acumulado entre o nó atual e o vizinho
                novo_custo = custos_acumulados[no_atual] + \
                             self.pega_peso(no_atual, vizinho)
                # se o novo custo for menor que o custo que já encontramos
                # antes, substitui
                if novo_custo < custos_acumulados[vizinho]:
                    # substituindo o custo para chegar no vizinho
                    custos_acumulados[vizinho] = novo_custo
                    # criando link entre o vizinho e o atual
                    pi[vizinho] = no_atual

        # com o laço finalizado, a busca acabou
        # nesse momento, precisamos criar o caminho entre o nó inicial
        # e o nó final (caminho inverso, ou seja, do fim pro começo)
        caminho = []
        custo_total = 1e10
        # encontrei um caminho? basicamente,
        # eu preciso verificar se o nó final tem um predecessor
        if pi[vertice_b] != None:
            # existe um caminho
            # obtendo o custo total
            custo_total = custos_acumulados[vertice_b]

            # montando o caminho ao "retornar" na estrutura de predecessores
            no_atual = vertice_b
            while no_atual != None:
                caminho.insert(0, no_atual)
                no_atual = pi[no_atual]

        # retorna o caminho e o custo
        return caminho, custo_total

    # Função que recebe a lista de vértices e os custos acumulados
    # O objetivo da função é encontrar o vértice com menor custo
    # acumulado até o momento
    def extract_min(self, q, pesos_acumulados):
        vertice_menor_custo = None
        min_weight = +1e10
        for vertice in q:
            if pesos_acumulados[vertice] <= min_weight:
                min_weight = pesos_acumulados[vertice]
                vertice_menor_custo = vertice
        return vertice_menor_custo

    def pega_vizinhos(self, vertice):
        if self.representacao == 'matriz':
            pass
        else:
            vizinhos = []
            if vertice in self.lista_vertices:
                for (vizinho, peso) in self.dict_vizinhos[vertice]:
                    vizinhos.append(vizinho)
            return vizinhos

    def pega_peso(self, vertice_a, vertice_b):
        if self.representacao == 'matriz':
            pass
        else:
            peso_encontrado = +1e10
            if vertice_a in self.lista_vertices and \
                    vertice_b in self.lista_vertices:
                for vizinho, peso in self.dict_vizinhos[vertice_a]:
                    if vizinho == vertice_b:
                        peso_encontrado = peso
                        break
            return peso_encontrado

    def busca_profundidade(self, vertice_inicial, vertice_final):
        # Muito importante: essa busca usa uma PILHA como base (stack)
        stack = []
        # lista de visitados
        visitados = []

        # adicionar o elemento inicial no FINAL da estrutura
        stack.append(vertice_inicial)

        # enquanto houverem elementos na estrutura
        while len(stack) > 0:
            # pega o último elemento da estrutura
            vertice_atual = stack.pop(-1)

            # adiciona o vertice atual nos visitados
            if vertice_atual not in visitados:
                visitados.append(vertice_atual)

            # adicionar os vizinhos na pilha
            for vizinho in sorted(self.pega_vizinhos(vertice_atual)):
                # se o vizinho ainda não foi visitado
                if vizinho not in visitados:
                    # adiciona ele na pilha
                    stack.append(vizinho)

            # verificar se não chegamos no vertice final
            if vertice_atual == vertice_final:
                break

        # retorno dos visitados
        return visitados

    def busca_largura(self, vertice_inicial, vertice_final):
        # Muito importante: essa busca usa uma FILA como base (queue)
        queue = []
        # lista de visitados
        visitados = []

        # adicionar o elemento inicial no FINAL da estrutura
        queue.append(vertice_inicial)

        # enquanto houverem elementos na estrutura
        while len(queue) > 0:
            # pega o primeiro elemento da estrutura
            vertice_atual = queue.pop(0)

            # adiciona o vertice atual nos visitados
            if vertice_atual not in visitados:
                visitados.append(vertice_atual)

            # adicionar os vizinhos na pilha
            for vizinho in sorted(self.pega_vizinhos(vertice_atual)):
                # se o vizinho ainda não foi visitado
                if vizinho not in visitados:
                    # adiciona ele na pilha
                    queue.append(vizinho)

            # verificar se não chegamos no vertice final
            if vertice_atual == vertice_final:
                break

        # retorno dos visitados
        return visitados

    def eh_conectado(self):
        # TODO: warshall
        # existe algum 0? -> não é conectado
        # caso contrário -> é conectado
        return True

    def prim(self):
    # TODO: implementar funcao que determina se o grafo é conexo ou não
        if self.eh_conectado():
            # lista de vertices e antecessores
            predecessores = {}
            pesos = {}
            for vertice in self.lista_vertices:
                predecessores[vertice] = None
                pesos[vertice] = 1e10

            # criando lista de vertices que existem no grafo original
            q = [x for x in self.lista_vertices]
            # q = []
            # for x in self.lista_vertices:
            #     q.append(x)

            while len(q) > 0:
                # encontrar o vértice ainda não adicionado
                # que tenha o menor peso
                u = self.extract_min(q, pesos)

                # remover esse vertice da lista
                q.remove(u)

                for vizinho in self.pega_vizinhos(u):
                    peso = self.pega_peso(u, vizinho)
                    if vizinho in q and peso < pesos[vizinho]:
                        predecessores[vizinho] = u
                        pesos[vizinho] = peso
            # monta novo grafo com as conexoes e pesos encontrados
            g_prim = Grafo(representacao=self.representacao,
                           direcionado=False,
                           ponderado=True)
            # copiar vertices originais
            for vertice in self.lista_vertices:
                g_prim.adiciona_vertice(vertice)

            # adiciona as arestas
            custo_acumulado = 0
            for vertice_inicio in predecessores.keys():
                vertice_final = predecessores[vertice_inicio]
                if vertice_final is not None:
                    g_prim.cria_aresta(vertice_inicio,
                                       vertice_final,
                                       pesos[vertice_inicio])
                    custo_acumulado += pesos[vertice_inicio]

            #retorna a MST
            return g_prim, custo_acumulado

    def __str__(self):
        ret =  f'Vértices: {self.lista_vertices}\n'
        ret += 'Arestas:\n'
        for vertice in self.dict_vizinhos.keys():
            ret += f'{vertice} \t {self.dict_vizinhos[vertice]}\n'
        return ret

if __name__ == '__main__':
    g = Grafo('lista',
              direcionado=False,
              ponderado=True)
    g.adiciona_vertice('A')
    g.adiciona_vertice('B')
    g.adiciona_vertice('C')
    g.adiciona_vertice('D')
    g.adiciona_vertice('E')
    g.cria_aresta('A','B', 2)
    g.cria_aresta('A','C', 4)
    g.cria_aresta('B','C', 6)
    g.cria_aresta('C','D', 1)
    g.cria_aresta('D','E', 2)
    g.cria_aresta('C','E', 3)
    print(g)
    print('Busca em Profundidade (A->E):')
    print(g.busca_profundidade('A', 'E'))

    print('Busca em Largura (A->E):')
    print(g.busca_largura('A', 'E'))

    print(g.lista_vertices)

    caminho, custo = g.dijkstra('A', 'E')
    print(f'Menor caminho entre A e E: {caminho} com custo = {custo}')
    print('Prim MST')
    g_mst, custo = g.prim()
    print(f'MST = {g_mst}\n custo = {custo}')




