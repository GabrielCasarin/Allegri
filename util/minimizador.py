# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import Estado, AutomatoFinito
from comum.automatos.estado import EstadoNaoDeterministico


def eliminar_transicoes_em_vazio(automato):
    def epsilon_closure(estado):
        fecho = [estado]
        pilha = list(fecho)
        while pilha:
            el = pilha.pop()
            if '' in el.simbolos:
                for el2 in el['']:
                    if el2 not in fecho:
                        fecho.append(el2)
                        pilha.append(el2)
        return fecho

    def delta1(qi, simbolo, fecho):
        D1 = []
        for qj in fecho:
            if simbolo in qj.simbolos:
                for qk in qj[simbolo]:
                    for el in epsilon_closure(qk):
                        if el not in D1:
                            D1.append(el)
        return D1

    for Si in automato:
        fecho = epsilon_closure(Si)
        for simbolo in automato.alfabeto:
            if simbolo != '':
                D1 = delta1(Si, simbolo, fecho)
                for el in D1:
                    Si[simbolo] = el
        for Sj in fecho:
            if not Si.final and Sj.final:
                Si.final = True

    for Si in automato:
        del Si['']


def eliminar_indeterminismos(automato):
    class EstadoContainer(EstadoNaoDeterministico):
        def __init__(self, conjunto_estados):
            # inicializa-se o objeto como um estado sem nome e não-final
            super(EstadoContainer, self).__init__(nome='')
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
        automato.estados[novo_estado.nome] = novo_estado
        for simbolo in novo_estado.transicoes.keys():
            if len(novo_estado[simbolo]) > 1:
                lista_indeterminismos.append((novo_estado, simbolo))
        for estado in automato:
            for simbolo in estado.transicoes.keys():
                if novo_estado.compara_conjunto(estado[simbolo]):
                    lista_indeterminismos.remove((estado, simbolo))
                    del estado[simbolo]
                    estado[simbolo] = novo_estado

    def converter_para_deterministico(automato):
        old_estados = automato.estados.values()
        automato.deterministico = True
        automato.estados = {}
        for q in old_estados:
            automato.add_estado(q.nome)
            automato[q.nome].final = q.final
            automato[q.nome].submaquinas_chamadas = q.submaquinas_chamadas
            for s in q.transicoes.keys():
                automato.add_estado(q[s][0].nome)
                automato[q.nome][s] = automato[q[s][0].nome]

    # cria uma lista inicial de indeterminismos
    lista_indeterminismos = []
    for estado in automato:
        for simbolo in estado.transicoes.keys():
            if len(estado[simbolo]) > 1:
                lista_indeterminismos.append((estado, simbolo))
    # itera por todos os indeterminismos
    while lista_indeterminismos:
        estado, simbolo = lista_indeterminismos[0]
        cria_novo_estado(estado[simbolo])
    # finalmente
    converter_para_deterministico(automato)


def eliminar_estados_inacessiveis(automato, inicial='q0'):
    estados = list(automato.estados.values())
    visitados = []
    pilha = [automato.estados[inicial]]
    while pilha:
        estadoAtual = pilha.pop()
        visitados.append(estadoAtual)
        for simbolo in estadoAtual.transicoes.keys():
            if automato.deterministico:
                proxEstado = estadoAtual[simbolo]
                if (proxEstado not in visitados
                    and proxEstado not in pilha):
                        pilha.insert(0, proxEstado)
            else: # se não é deterministico
                for proxEstado in estadoAtual[simbolo]:
                    if (proxEstado not in visitados
                        and proxEstado not in pilha):
                            pilha.insert(0, proxEstado)
    a_serem_removidos = [q.nome for q in estados if q not in visitados]
    for estado in a_serem_removidos:
        del automato.estados[estado]


def minimizador_de_Hopcroft(automato):
    '''Retorna uma partição do conjunto de estados de um autômato
       correspondente às classes de equivalência obtidas segundo
       o algoritmo de minimização de Hopcroft.'''
    def delta_R(P, a):
        conj = []
        for q in automato:
            if a in q.simbolos and q[a] in P:
                conj.append(q)
        return conj

    Grupos = [[],[]]
    for q in automato:
        if q.final:
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


def particao_para_automato_finito(nome, alfabeto, particao, inicial='q0'):
    def acha(nome_estado):
        for i in range(len(particao)):
            for estado in particao[i]:
                if estado.nome == nome_estado:
                    return i
        return None

    af = AutomatoFinito(nome=nome, estados=[inicial], estadoInicial=inicial, alfabeto=alfabeto)

    pilha = []
    # finais = []

    i = acha(inicial)
    nomes_classes = {
        i: inicial
    }

    pilha.append(particao[i][0])

    cont = 0
    while pilha:
        estado_atual = pilha.pop()
        j = acha(estado_atual.nome)
        qi = nomes_classes[j]
        for s, qj in estado_atual.transicoes.items():
            if qj is not None:
                # acha o indice do conjunto, dentro da partição, a que pertence qj
                i = acha(qj.nome)
                if not i in nomes_classes:
                    cont += 1
                    nova_classe = 'q' + str(cont)
                    nomes_classes[i] = nova_classe
                    pilha.append(particao[i][0])
                    af.add_estado(nova_classe)
                # print("({}, '{}') -> {}".format(nomes_classes[acha(estado_atual.nome)], s, nomes_classes[acha(qj.nome)]))
                af.add_transicao(de=qi, com=s, para=nomes_classes[i])
        af[qi].final = estado_atual.final
        af[qi].submaquinas_chamadas = estado_atual.submaquinas_chamadas
    # print("F =", finais)
    return af
