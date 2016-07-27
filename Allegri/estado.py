# coding=utf-8


class Estado(object):
    """representa um Estado com suas transições"""
    def __init__(self, nome, final=False):
        super(Estado, self).__init__()
        self._nome = nome
        self._transicoes = {}
        self._final = final

    def setFinal(self):
        self._final = True

    def isFinal(self):
        return self._final

    def simbolos(self):
        return self._transicoes.keys()

    def __setitem__(self, simbol, prox):
        self._transicoes[simbol] = prox

    def __getitem__(self, simbol):
    	return self._transicoes[simbol]

    def __eq__(self, estado):
    	if isinstance(estado, Estado):
    		return self == estado._nome
    	else:
    		return self._nome == estado

    def __contains__(self, item):
        return item in self._transicoes.keys()

    def __str__(self):
        return self._nome
