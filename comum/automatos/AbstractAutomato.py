# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.

from . import Estado


class AbstractAutomato:
    def __init__(self, deterministico=True):
        super(AbstractAutomato, self).__init__()
        self.alfabeto = []
        self.estados = {}
        self.deterministico = deterministico

    def __getitem__(self, estado):
        if estado not in self.estados:
            self.estados[estado] = Estado(estado, deterministico=self.deterministico)
        return self.estados[estado]

    def _gerarAlfabeto(self):
        for q in self.estados.values():
            for s in q.simbolos():
                # self._adicionarSimbolo(s)
                if s not in self.alfabeto:
                    self.alfabeto.append(s)
        for q in self.estados.values():
            for s in self.alfabeto:
                if s not in q: q[s] = ''
