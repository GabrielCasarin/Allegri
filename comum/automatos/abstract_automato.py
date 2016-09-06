# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from . import Estado


class AbstractAutomato:
    def __init__(self, deterministico=True):
        super(AbstractAutomato, self).__init__()
        self.alfabeto = set()
        self.estados = {}
        self.deterministico = deterministico

    def add_transicao(self, de, com, para):
        if de not in self.estados:
            self.estados[de] = Estado(de, deterministico=self.deterministico)
        if para not in self.estados:
            self.estados[para] = Estado(para, deterministico=self.deterministico)
        self.estados[de][com] = self.estados[para]
        self._gerarAlfabeto()

    def _gerarAlfabeto(self):
        for q in self.estados.values():
            for s in q.simbolos():
                self.alfabeto.add(s)
        for q in self.estados.values():
            for s in self.alfabeto:
                if s not in q:
                    q[s] = None
