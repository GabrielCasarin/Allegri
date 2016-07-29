# coding=utf-8
# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import itertools

from Allegri import Estado
from Allegri.minimizador import eliminar_transicoes_em_vazio, eliminar_indeterminismos

def transforma_em_str(estados1):
    temp = []
    for estado in estados1:
        nomeEstado = estado.nome
        for simbolo in estado.simbolos():
            transicao = "({0}, {1}) -> {2}".format(nomeEstado, simbolo, estado[simbolo][0])
            temp.append(transicao)
    return "{" + ', \n'.join(temp) + "}"

def main():
    regra = "X=ab(cd|ef)|[g|h{ij|k}]{m}|{n}."
    pilha = []
    transicoes = []
    contador = itertools.count()
    valor_atual = next(contador)
    estado = valor_atual

    # for token in regra:
    print("Átomo estado contador   Pilha                          transições")
    i = 0
    while i < len(regra):
        if regra[i] == 'X':
            valor_atual = next(contador)
            transicoes.append((valor_atual, '', 'pop()'))

        elif regra[i] == '=':
            pilha.append((estado, valor_atual))
            valor_atual = next(contador)

        elif regra[i] in 'abcdefghijkmn':
            estado_anterior = estado
            estado = valor_atual
            valor_atual = next(contador)
            transicoes.append((estado_anterior, regra[i], estado))

        elif regra[i] == '(':
            pilha.append((estado, valor_atual))
            valor_atual = next(contador)

        elif regra[i] == ')':
            estadoAtual, proxEstado = pilha.pop()
            transicoes.append((estado, '', proxEstado))
            estado = proxEstado

        elif regra[i] == '[':
            pilha.append((estado, valor_atual))
            transicoes.append((estado, '', valor_atual))
            valor_atual = next(contador)

        elif regra[i] == ']':
            estadoAtual, proxEstado = pilha.pop()
            transicoes.append((estado, '', proxEstado))
            estado = proxEstado

        elif regra[i] == '{':
            transicoes.append((estado, '', valor_atual))
            estado = valor_atual
            pilha.append((estado, estado))
            valor_atual = next(contador)

        elif regra[i] == '}':
            estadoAtual, proxEstado = pilha.pop()
            transicoes.append((estado, '', estadoAtual))
            estado = estadoAtual

        elif regra[i] == '|':
            estadoAtual, proxEstado = pilha[-1]
            transicoes.append((estado, '', proxEstado))
            estado = estadoAtual

        elif regra[i] == '.':
            estadoAtual, proxEstado = pilha[-1]
            transicoes.append((estado, '', proxEstado))

        print("{atomo:>5} {estado:>6} {contador:>8}   {pilha:<30} {transicoes:<25}".format(atomo=regra[i], estado=estado, contador=valor_atual, pilha=repr(pilha), transicoes=repr(transicoes[-1])))
        i += 1

    # gera os estados
    tabela = {}
    for id_estado, simb, id_proxEstado in transicoes:
        nomeEstado = 'q' + str(id_estado)
        if nomeEstado not in tabela:
            tabela[nomeEstado] = Estado(nomeEstado)
        if id_proxEstado != 'pop()':
            nomeProxEstado = 'q' + str(id_proxEstado)
            if nomeProxEstado not in tabela:
                tabela[nomeProxEstado] = Estado(nomeProxEstado)
            tabela[nomeEstado][simb] = tabela[nomeProxEstado]
        else:
            tabela[nomeEstado].setFinal()

    # print('antes')
    keys = list(tabela.keys())
    keys.sort()
    estados1 = [ tabela[key] for key in keys ]

    # for el in keys:
    #     print(el, ' {', end='')
    #     for fl in tabela[el]._transicoes:
    #         print(fl,': [', end='')
    #         for gl in tabela[el]._transicoes[fl]:
    #             print(gl, ', ', sep='', end='')
    #         print('], ', end='')
    #     print('}')


    eliminar_transicoes_em_vazio(estados1)

    # print('depois')
    # keys = list(tabela.keys())
    # keys.sort()
    # for el in keys:
    #     print(el, ' {', end='')
    #     for fl in tabela[el]._transicoes:
    #         print(fl,': [', end='')
    #         for gl in tabela[el]._transicoes[fl]:
    #             print(gl, ', ', sep='', end='')
    #         print('], ', end='')
    #     print('}')
    print('Q = {', estados1, '}')
    print('d =', transforma_em_str(estados1))
    finais = [estado for estado in estados1 if estado.isFinal()]
    print(finais)

if __name__ == '__main__':
    main()
