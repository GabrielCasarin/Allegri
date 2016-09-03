# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import Estado


def gera_tabela(transicoes):
    tabela = {}
    for id_estado, simb, id_proxEstado in transicoes:
        nomeEstado = 'q' + str(id_estado)
        if nomeEstado not in tabela:
            tabela[nomeEstado] = Estado(nomeEstado, deterministico=False)
        if id_proxEstado != 'pop()':
            nomeProxEstado = 'q' + str(id_proxEstado)
            if nomeProxEstado not in tabela:
                tabela[nomeProxEstado] = Estado(nomeProxEstado, deterministico=False)
            tabela[nomeEstado][simb] = tabela[nomeProxEstado]
        else:
            tabela[nomeEstado].setFinal()
    return tabela

def eliminar_transicoes_em_vazio(estados, alfabeto):
    def epsilon_closure(estado):
        fecho = [estado]
        pilha = list(fecho)
        while pilha:
            el = pilha.pop()
            if '' in el:
                for el2 in el['']:
                    if el2 not in fecho:
                        fecho.append(el2)
                        pilha.append(el2)
        return fecho

    def delta1(qi, simbolo):
        D1 = []
        fecho = epsilon_closure(qi)
        for qj in fecho:
            if simbolo in qj:
                for qk in qj[simbolo]:
                    for el in epsilon_closure(qk):
                        if el not in D1:
                            D1.append(el)
                        if not qi.isFinal() and el.isFinal():
                            qi.setFinal()
        for el in D1:
            qi[simbolo] = el

    for Si in estados:
        # print(Si)
        for simbolo in alfabeto:
            if simbolo != '':
                # print('antes', simbolo, Si._transicoes)
                delta1(Si, simbolo)
                # print('depois', simbolo, Si._transicoes)

    for Si in estados:
        Si.removeSimbolo('')

def eliminar_indeterminismos(estados1):
    class EstadoContainer(Estado):
        def __init__(self, conjunto_estados):
            # inicializa-se o objeto como um estado sem nome e não-final
            super(EstadoContainer, self).__init__('', deterministico=False)
            # a idéia aqui é encontrar os estados-raiz de cada elemento de conjunto_estados
            self.conjunto_estados = []
            for el in conjunto_estados:
                if isinstance(el, EstadoContainer):
                    for estado in el.conjunto_estados:
                        if estado not in self.conjunto_estados:
                            self.conjunto_estados.append(estado)
                elif isinstance(el, Estado):
                    if el not in self.conjunto_estados:
                        self.conjunto_estados.append(el)

            self.conjunto_estados = sorted(self.conjunto_estados, key=lambda e: e.nome)

            for estado in self.conjunto_estados:
                self.nome += estado.nome
                self.merge(estado, True)

        def compara_conjunto(self, conjunto_estados):
            temp = list(conjunto_estados)
            for el in conjunto_estados:
                if isinstance(el, EstadoContainer):
                    temp.remove(el)
                    for estado in el.conjunto_estados:
                        if estado not in temp:
                            temp.append(estado)
            # print('nome:', self.nome, 'conjunto_estados:', temp)
            if len(self.conjunto_estados) == len(temp):
                for el in self.conjunto_estados:
                    if el not in temp:
                        return False
                return True
            else:
                return False

    def cria_novo_estado(conjunto_estados):
        """
        cria um novo estado a partir da fusao de dois ou mais outros
        """
        novo_estado = EstadoContainer(conjunto_estados)
        estados2.append(novo_estado)
        tabela[novo_estado.nome] = novo_estado
        for simbolo in novo_estado.simbolos():
            if len(novo_estado[simbolo]) > 1:
                lista_indeterminismos.append((novo_estado, simbolo))
        for estado in estados2:
            for simbolo in estado.simbolos():
                if novo_estado.compara_conjunto(estado[simbolo]):
                    lista_indeterminismos.remove((estado, simbolo))
                    estado.removeSimbolo(simbolo)
                    estado[simbolo] = novo_estado

    estados2 = list(estados1)
    tabela = {
        str(estado) : estado for estado in estados2
    }

    # cria uma lista inicial de indeterminismos
    lista_indeterminismos = []
    for estado in estados2:
        for simbolo in estado.simbolos():
            if len(estado[simbolo]) > 1:
                lista_indeterminismos.append((estado, simbolo))
    print('lista de indeterminismos inicial', lista_indeterminismos)
    while lista_indeterminismos:
        estado, simbolo = lista_indeterminismos[0]
        cria_novo_estado(estado[simbolo])

    return estados2

def eliminar_estados_inacessiveis(estados, inicial):
    visitados = []
    pilha = [inicial]
    while pilha:
        estadoAtual = pilha.pop()
        # if estadoAtual not in visitados:
        visitados.append(estadoAtual)
        for simbolo in estadoAtual.simbolos():
            for proxEstado in estadoAtual[simbolo]:
                if (proxEstado not in visitados
                    and proxEstado not in pilha):
                        pilha.insert(0, proxEstado)
    return visitados

def minimizador_Hopcroft(automato):
    '''Retorna uma partição das classes de equivalência do conjunto de estados de um autômato'''
    def delta_R(P, a):
        conj = []
        for q in automato.estados.values():
            if a in q and q[a] in P:
                conj.append(q)
        return conj

    Grupos = [[],[]]
    for q in automato.estados.values():
        if q.isFinal():
         Grupos[1].append(q)
        else:
         Grupos[0].append(q)

    Ativo = [list(Grupos[1])]

    while Ativo:
        A = Ativo.pop()
        for a in automato.alfabeto:
            for G in Grupos:
                delta = delta_R(A, a)
                # G1 = G inter delta
                G1 = [x for x in G if x in delta]
                # G2 = G - G1
                G2 = [x for x in G if x not in G1]

                if G1 and G2:
                    Grupos.remove(G)
                    Grupos.append(G1)
                    Grupos.append(G2)
                    if G in Ativo:
                        Ativo.remove(G)
                        Ativo.append(G1)
                        Ativo.append(G2)
                    else:
                        if len(G1) < len(G2):
                            Ativo.append(G1)
                        else:
                            Ativo.append(G2)

    return Grupos
