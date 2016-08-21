# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import itertools

from Allegri import Estado
from Allegri.minimizador import eliminar_transicoes_em_vazio, eliminar_indeterminismos, eliminar_estados_inacessiveis

def transforma_em_str(estados):
    temp = []
    for estado in estados:
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
    # print("Átomo estado contador   Pilha                          transições")
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

        # print("{atomo:>5} {estado:>6} {contador:>8}   {pilha:<30} {transicoes:<25}".format(atomo=regra[i], estado=estado, contador=valor_atual, pilha=repr(pilha), transicoes=repr(transicoes[-1])))
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

    keys = list(tabela.keys())
    keys.sort()
    estados1 = [ tabela[key] for key in keys ]

    eliminar_transicoes_em_vazio(estados1, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n'])
    estados2 = eliminar_indeterminismos(estados1)
    estados3 = eliminar_estados_inacessiveis(estados2, tabela['q0'])

    print('Q = {', estados3, '}')
    print('d =', transforma_em_str(estados3))
    finais = [estado for estado in estados3 if estado.isFinal()]
    print(finais)
    inacessiveis = [x for x in estados2 if x not in estados3]
    print(inacessiveis)

class MetaReconhecedor(object):
    """Meta-reconhecedor"""
    def __init__(self):
        super(MetaReconhecedor, self).__init__()

        ## pilha que determina o escopo em que está o pé da análise
        self.pilha = []

        ## conjunto de transições obtidas pela análise do conjunto de regras da gramática
        self.transicoes = []

        self.contador = itertools.count()


    def nao_terminal(self):
        self.valor_atual = next(self.contador)
        self.transicoes.append((self.valor_atual, '', 'pop()'))

    def terminal(self, token_value):
        estado_anterior = self.estado
        self.estado = self.valor_atual
        self.valor_atual = next(self.contador)
        self.transicoes.append((estado_anterior, token_value, self.estado))

    def igual(self):
        self.pilha.append((self.estado, self.valor_atual))
        self.valor_atual = next(self.contador)

    def lparen(self):
            self.pilha.append((self.estado, self.valor_atual))
            self.valor_atual = next(self.contador)

    def rparen(self):
            estadoAtual, proxEstado = self.pilha.pop()
            self.transicoes.append((self.estado, '', proxEstado))
            self.estado = proxEstado

    def lcolchete(self):
            self.pilha.append((self.estado, self.valor_atual))
            self.transicoes.append((self.estado, '', self.valor_atual))
            self.valor_atual = next(self.contador)

    def rcolchete(self):
            estadoAtual, proxEstado = self.pilha.pop()
            self.transicoes.append((estado, '', proxEstado))
            self.estado = proxEstado

    def lchave(self):
            self.transicoes.append((self.estado, '', self.valor_atual))
            self.estado = valor_atual
            self.pilha.append((self.estado, self.estado))
            self.valor_atual = next(self.contador)

    def rchave(self):
            estadoAtual, proxEstado = self.pilha.pop()
            self.transicoes.append((self.estado, '', estadoAtual))
            self.estado = estadoAtual

    def barra_vertical(self):
            estadoAtual, proxEstado = self.pilha[-1]
            self.transicoes.append((self.estado, '', proxEstado))
            self.estado = estadoAtual

    def ponto_final(self):
            estadoAtual, proxEstado = self.pilha[-1]
            self.transicoes.append((self.estado, '', proxEstado))

def tokenizer(cadeia):
    from Allegri.MetaReconhecedor import AutomatoFinito

    reconhecedor = AutomatoFinito('reconhecedor')

if __name__ == '__main__':
    main()
