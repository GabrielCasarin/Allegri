# coding=utf-8
# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from Allegri import *

alfabeto = ['a', 'b', 'c', '']

estados1 = [
    Estado('q0'),
    Estado('q1', True),
    Estado('q2', True),
    Estado('q3', True),
]

tabela = {
    str(estado) : estado for estado in estados1
}

# tabela['q0']['a'] = tabela['q1']
# tabela['q0']['a'] = tabela['q2']
#
# tabela['q2']['a'] = tabela['q0']
# tabela['q2']['a'] = tabela['q2']
# tabela['q2']['b'] = tabela['q0']
# tabela['q2']['b'] = tabela['q1']


tabela['q0']['a'] = tabela['q1']
tabela['q0']['a'] = tabela['q2']
tabela['q0']['c'] = tabela['q3']

tabela['q1']['a'] = tabela['q0']
tabela['q1']['b'] = tabela['q0']
tabela['q1']['b'] = tabela['q1']

tabela['q2']['c'] = tabela['q2']

tabela['q3']['a'] = tabela['q2']
tabela['q3']['b'] = tabela['q1']

def eliminar_transicoes_em_vazio():
    # estado qualquer Si
    for Si in estados1:
        # se houver transicoes em vazio de Si para Sj, dá merge
        if '' in Si:
            for Sj in Si['']:
                Si.merge(Sj)
                # e transforma Si em estado final, caso Sj o seja
                if Sj.isFinal():
                    Si.setFinal()
        # elimina-se as coluna desnecessarias
        Si.removeSimbolo('')

def eliminar_indeterminismos():
    estados2 = list(estados1)

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
    # i = 6
    while lista_indeterminismos:
    # while i > 0:
        estado, simbolo = lista_indeterminismos[0]
        cria_novo_estado(estado[simbolo])
        # i-=1
    estados1 = estados2

print('antes')
for el in tabela:
    print(el, ' {', end='')
    for fl in tabela[el]._transicoes:
        print(fl,': [', end='')
        for gl in tabela[el]._transicoes[fl]:
            print(gl, ', ', sep='', end='')
        print('], ', end='')
    print('}')

eliminar_indeterminismos()

print('depois')
for el in tabela:
    print(el, ' {', end='')
    for fl in tabela[el]._transicoes:
        print(fl,': [', end='')
        for gl in tabela[el]._transicoes[fl]:
            print(gl, ', ', sep='', end='')
        print('], ', end='')
    print('}')
