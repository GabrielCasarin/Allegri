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
        if com != '':
            self._gerarAlfabeto()

    def add_estado(self, nome_estado, final=False):
        if nome_estado not in self.estados:
            self.estados[nome_estado] = Estado(nome_estado, final, self.deterministico)

    def _gerarAlfabeto(self):
        for q in self.estados.values():
            for s in q.simbolos():
                if s != '':
                    self.alfabeto.add(s)
        for q in self.estados.values():
            for s in self.alfabeto:
                if self.deterministico and s not in q:
                    q[s] = None

    def __getitem__(self, nome_estado):
        if nome_estado in self.estados:
            return self.estados[nome_estado]
        else:
            return None
