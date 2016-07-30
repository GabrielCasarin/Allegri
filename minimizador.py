# coding=utf-8
# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from Allegri import *


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
        for simbolo in alfabeto:
            if simbolo != '':
                delta1(Si, simbolo)
    for Si in estados:
        Si.removeSimbolo('')

def eliminar_indeterminismos(estados1):
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

