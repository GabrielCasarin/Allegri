# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from . import Estado


class AbstractAutomato:
    def __init__(self, deterministico=True):
        super(AbstractAutomato, self).__init__()
        self.alfabeto = set()
        self.estados = {}
        self.deterministico = deterministico

    def add_estado(self, nome_estado, final=False):
        if nome_estado not in self.estados:
            self.estados[nome_estado] = Estado(nome_estado, final, self.deterministico)

    def add_transicao(self, de, com, para):
        self.add_estado(de)
        self.add_estado(para)
        self.estados[de][com] = self.estados[para]
        if com != '':
            self.gerar_alfabeto()

    def gerar_alfabeto(self):
        for q in self.estados.values():
            for s in q._transicoes.keys():
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
