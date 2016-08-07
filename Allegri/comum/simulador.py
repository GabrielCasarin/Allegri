# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from . lista_encadeada import ListaEncadeada


class Simulador:
    def __init__(self):
        super(Simulador, self).__init__()
        self.__listaEventos = ListaEncadeada()

    def trata_evento(self, evento):
        pass

    def add_evento(self, evento):
        self.__listaEventos.insere(evento)

    def run(self):
        while self.__listaEventos:
            proximo_evento = self.__listaEventos.remove()
            self.trata_evento(proximo_evento)
