# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


class Estado:
    """representa um Estado com suas transições"""
    def __init__(self, nome, final=False, deterministico=True):
        super(Estado, self).__init__()
        self.nome = nome
        self._transicoes = {}
        self._final = final
        self.eh_deterministico = deterministico

    def setFinal(self):
        self._final = True

    def isFinal(self):
        return self._final

    def simbolos(self):
        return self._transicoes.keys()

    def merge(self, Sj, com_transicoes_em_vazio=False):
        if not self.eh_deterministico:
            for simbolo in Sj.simbolos():
                if com_transicoes_em_vazio or (not com_transicoes_em_vazio and simbolo != ''):
                    if simbolo in self._transicoes:
                        for estado_destinho in Sj[simbolo]:
                            if estado_destinho not in self._transicoes[simbolo]:
                                self._transicoes[simbolo].append(estado_destinho)
                    else:
                        if simbolo in Sj._transicoes:
                            self._transicoes[simbolo] = list(Sj[simbolo])
            if Sj.isFinal():
                self.setFinal()

    def removeSimbolo(self, simbolo):
        if simbolo in self._transicoes:
            del self._transicoes[simbolo]

    def __setitem__(self, simbolo, prox):
        if not self.eh_deterministico:
            if simbolo not in self._transicoes:
                self._transicoes[simbolo] = [prox]
            elif prox not in self._transicoes[simbolo]:
                self._transicoes[simbolo].append(prox)
        else:  # se for determinístico
            self._transicoes[simbolo] = prox

    def __getitem__(self, simbolo):
        return self._transicoes[simbolo]

    def __eq__(self, estado):
        if isinstance(estado, Estado):
            return self == estado.nome
        else:
            return self.nome == estado

    def __contains__(self, item):
        return item in self._transicoes.keys()

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.nome
