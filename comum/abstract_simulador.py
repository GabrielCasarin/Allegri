# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from . lista_encadeada import ListaEncadeada


class AbstractSimulador:
    def __init__(self):
        super(AbstractSimulador, self).__init__()
        self._listaEventos = ListaEncadeada()

    def trata_evento(self, evento):
        pass

    def add_evento(self, evento, fim=False):
        if fim:
            self._listaEventos.insere_no_fim(evento)
        else:
            self._listaEventos.insere(evento)

    def run(self):
        while self._listaEventos:
            proximo_evento = self._listaEventos.remove()
            self.trata_evento(proximo_evento)
