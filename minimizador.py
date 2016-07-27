# coding=utf-8
# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.

from Allegri import Estado

alfabeto = ['a', 'b', '']
estados = {'q0': Estado('q0'), 'q1': Estado('q1', True)}
estados['q0']['a'] = estados['q0']
estados['q0'][''] = estados['q1']
estados['q1']['b'] = estados['q1']

tabela = {
    estado : {} for estado in estados
}

for estado in estados:
    for simbolo in alfabeto:
        tabela[estado][simbolo] = set()

for estado in estados:
    for simbolo in estados[estado].simbolos():
        tabela[estado][simbolo].add(
            str(estados[estado][simbolo])
        )


def eliminar_transicoes_em_vazio():
    # estado qualquer Si
    for Si in tabela:
        # se houver transicoes em vazio de Si para Sj, dá merge
        for Sj in tabela[Si]['']:
            merge(Si, Sj)
            # e transforma Si em estado final, caso Sj o seja
            if estados[Sj].isFinal():
                estados[Si].setFinal()
    for estado in estados:
        # elimina-se as coluna desnecessarias
        del tabela[estado]['']

def merge(Si, Sj, com_transicoes_em_vazio=False):
    """dá um merge entre Sj e Si, copiando as transicoes de Sj para Si"""
    for simbolo in tabela[Sj]:
        if com_transicoes_em_vazio:
            tabela[Si][simbolo] |= tabela[Sj][simbolo]
        elif simbolo != '':
            tabela[Si][simbolo] |= tabela[Sj][simbolo]

print('depois')
print('q0 <- ', end='')
print(tabela['q0'])
print('q1 <- ', end='')
print(tabela['q1'])

eliminar_transicoes_em_vazio()

print('depois')
print('q0 <- ', end='')
print(tabela['q0'])
print('q1 <- ', end='')
print(tabela['q1'])
