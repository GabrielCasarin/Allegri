# coding=utf-8
# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import itertools

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

if __name__ == '__main__':
    main()
