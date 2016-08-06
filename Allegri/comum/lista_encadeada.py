# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


class No(object):
    def __init__(self, conteudo):
        super(No, self).__init__()
        self.conteudo = conteudo
        self.proximo = None


class ListaEncadeada(object):
    def __init__(self):
        super(ListaEncadeada, self).__init__()
        self.raiz = None
        self.__length = 0

    def insere(self, conteudo):
        novoNo = No(conteudo)
        if self.raiz is None:
            self.raiz = novoNo
        else:
            # busca o último No
            noAtual = self.raiz
            while noAtual.proximo is not None:
                noAtual = noAtual.proximo
            # insere o novo No
            noAtual.proximo = novoNo

    def remove(self):
        noAntigo = self.raiz
        if self.raiz is not None:
            self.raiz = self.raiz.proximo
            noAntigo.proximo = None
        return noAntigo
